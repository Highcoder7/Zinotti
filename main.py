import asyncio
import logging
import io
import os
from PIL import Image
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, BufferedInputFile, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from google import genai
from google.genai import types

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8769687821:AAEu9aGSIwkiVYBhx3IoT3vBrOEBD0OXQck")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyD7Wh_aDSLXzFo0ecTuTNVIRYLdaQg_sp4")
GEMINI_MODEL = "gemini-3.1-flash-image-preview"

FURNITURE_TYPES = [
    "Кухня", "Ванная", "Шкаф", "Шкафы купе",
    "Прихожая", "Спальня", "Гардероб", "ТВ-зона",
]

SYSTEM_PROMPT = (
    "Ты профессиональный ИИ-дизайнер интерьера компании Zinotti. "
    "На основе предоставленного фото (комната, чертёж или 3D-эскиз) создай "
    "фотореалистичный рендер интерьера с мебелью типа: {furniture_type}. "
    "Требования: photorealistic, 8K, interior design magazine style, "
    "мебель точно вписана в геометрию и перспективу, профессиональное освещение. "
    "Если подан чертёж или 3D — преврати его в фотореалистичный рендер. "
    "Пожелания клиента: {description}"
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

gemini_client = genai.Client(api_key=GEMINI_API_KEY)


class Flow(StatesGroup):
    waiting_for_photo = State()
    waiting_for_description = State()
    generated = State()


def furniture_keyboard() -> InlineKeyboardMarkup:
    rows = []
    for i in range(0, len(FURNITURE_TYPES), 2):
        pair = FURNITURE_TYPES[i:i + 2]
        rows.append([InlineKeyboardButton(text=t, callback_data=f"furniture:{t}") for t in pair])
    rows.append([InlineKeyboardButton(text="🔁 СТАРТ", callback_data="restart")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def result_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Ещё варианты", callback_data="more")],
        [InlineKeyboardButton(text="🔁 СТАРТ", callback_data="restart")],
    ])


def generate_interior(furniture_type: str, image_bytes: bytes, description: str) -> bytes | None:
    prompt = SYSTEM_PROMPT.format(furniture_type=furniture_type, description=description)
    pil_image = Image.open(io.BytesIO(image_bytes))

    response = gemini_client.models.generate_content(
        model=GEMINI_MODEL,
        contents=[prompt, pil_image],
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
        ),
    )

    logger.info("Gemini response parts: %d", len(response.parts))
    for i, part in enumerate(response.parts):
        is_thought = getattr(part, "thought", False)
        logger.info("Part %d: thought=%s text=%s has_image=%s", i, is_thought, bool(part.text), bool(part.as_image()))

    for part in response.parts:
        if getattr(part, "thought", False):
            continue
        img = part.as_image()
        if img:
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            return buf.getvalue()

    return None


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


async def send_type_selection(target: Message | CallbackQuery, state: FSMContext):
    await state.clear()
    text = (
        "👋 Добро пожаловать в <b>Zinotti</b>!\n\n"
        "Я ИИ-дизайнер интерьера. Загрузите фото комнаты, чертёж или 3D-эскиз "
        "— и я покажу, как будет выглядеть готовый результат.\n\n"
        "Выберите тип мебели:"
    )
    if isinstance(target, CallbackQuery):
        await target.message.answer(text, reply_markup=furniture_keyboard(), parse_mode="HTML")
    else:
        await target.answer(text, reply_markup=furniture_keyboard(), parse_mode="HTML")


@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await send_type_selection(message, state)


@dp.callback_query(F.data == "restart")
async def cb_restart(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await send_type_selection(callback, state)


@dp.callback_query(F.data.startswith("furniture:"))
async def cb_furniture(callback: CallbackQuery, state: FSMContext):
    furniture_type = callback.data.split(":", 1)[1]
    await state.update_data(furniture_type=furniture_type)
    await state.set_state(Flow.waiting_for_photo)
    await callback.answer()
    await callback.message.answer(
        f"✅ Выбрано: <b>{furniture_type}</b>\n\n"
        "📷 Пришлите фото комнаты, чертёж или 3D-эскиз.",
        parse_mode="HTML",
    )


@dp.message(Flow.waiting_for_photo, F.photo)
async def handle_photo(message: Message, state: FSMContext):
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    file_io = await bot.download_file(file.file_path)
    await state.update_data(image=file_io.read())
    await state.set_state(Flow.waiting_for_description)
    await message.answer("✏️ Опишите, что нужно добавить (на русском).")


@dp.message(Flow.waiting_for_photo)
async def handle_photo_wrong(message: Message):
    await message.answer("📷 Пожалуйста, отправьте фото комнаты, чертёж или 3D-эскиз.")


@dp.message(Flow.waiting_for_description, F.text)
async def handle_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(Flow.generated)
    await run_generation(message, state)


@dp.message(Flow.waiting_for_description)
async def handle_description_wrong(message: Message):
    await message.answer("✏️ Пожалуйста, опишите пожелания текстом.")


@dp.callback_query(F.data == "more", Flow.generated)
async def cb_more(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await run_generation(callback.message, state, is_callback=True)


async def run_generation(message: Message, state: FSMContext, is_callback: bool = False):
    data = await state.get_data()
    furniture_type = data.get("furniture_type", "")
    image_bytes = data.get("image")
    description = data.get("description", "")

    processing = await message.answer("⏳ Генерирую ваши варианты...")

    try:
        result = await asyncio.wait_for(
            asyncio.to_thread(generate_interior, furniture_type, image_bytes, description),
            timeout=120,
        )

        await bot.delete_message(message.chat.id, processing.message_id)

        if result:
            await message.answer_photo(
                BufferedInputFile(result, filename="zinotti_design.png"),
                caption="✅ Ваши готовые варианты.\n\nНажмите, если хотите другие варианты.",
                reply_markup=result_keyboard(),
            )
        else:
            await message.answer(
                "Не удалось сгенерировать изображение. Попробуйте снова.",
                reply_markup=result_keyboard(),
            )
    except asyncio.TimeoutError:
        logger.error("Generation timed out after 120s")
        try:
            await bot.delete_message(message.chat.id, processing.message_id)
        except Exception:
            pass
        await message.answer(
            "⏱ Генерация заняла слишком долго. Попробуйте снова.",
            reply_markup=result_keyboard(),
        )
    except Exception as e:
        import traceback
        logger.error(f"Generation error: {e}\n{traceback.format_exc()}")
        try:
            await bot.delete_message(message.chat.id, processing.message_id)
        except Exception:
            pass
        await message.answer(
            f"Произошла ошибка:\n<code>{e}</code>\n\nПопробуйте ещё раз.",
            reply_markup=result_keyboard(),
            parse_mode="HTML",
        )


async def main():
    logger.info("Zinotti bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
