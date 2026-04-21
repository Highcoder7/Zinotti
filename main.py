import asyncio
import logging
import io
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, BufferedInputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from google import genai
from google.genai import types

BOT_TOKEN = os.environ["BOT_TOKEN"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
GEMINI_MODEL = "gemini-3.1-flash-image-preview"

SYSTEM_PROMPT = """Ты профессиональный ИИ-дизайнер интерьера для мебельной компании.
Твоя задача — обставить комнату мебелью согласно описанию пользователя.
Требования к результату:
- Фотореалистичное изображение высокого качества (8K, photorealistic)
- Мебель должна точно вписываться в геометрию и перспективу комнаты
- Учитывай пожелания по стилю, цвету и материалам
- Красивое, профессиональное освещение
- Стиль: interior design magazine, architectural photography"""

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

gemini_client = genai.Client(api_key=GEMINI_API_KEY)


class DesignFlow(StatesGroup):
    waiting_for_description = State()


def generate_interior(description: str, image_bytes: bytes | None = None) -> bytes | None:
    parts = []

    if image_bytes:
        parts.append(types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"))

    full_prompt = f"{SYSTEM_PROMPT}\n\nЗапрос пользователя: {description}"
    parts.append(types.Part.from_text(text=full_prompt))

    contents = [types.Content(role="user", parts=parts)]

    response = gemini_client.models.generate_content(
        model=GEMINI_MODEL,
        contents=contents,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE", "TEXT"],
        ),
    )

    for part in response.candidates[0].content.parts:
        if part.inline_data:
            return part.inline_data.data

    return None


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Привет! Я ИИ-дизайнер интерьера 🛋\n\n"
        "Отправь мне:\n"
        "📷 *Фото комнаты* — и я обставлю её мебелью\n"
        "✏️ *Только текст* — и я создам дизайн с нуля\n\n"
        "Пример: \"Белая кухня в стиле минимализм с подсветкой\"",
        parse_mode="Markdown",
    )


@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "Как пользоваться ботом:\n\n"
        "1️⃣ Отправь фото пустой комнаты или эскиз\n"
        "2️⃣ Опиши желаемый стиль (цвет, материалы, стиль)\n"
        "3️⃣ Получи фотореалистичный рендер с мебелью\n\n"
        "Команды:\n"
        "/start — начать заново\n"
        "/help — эта справка"
    )


@dp.message(F.photo)
async def handle_photo(message: Message, state: FSMContext):
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    file_bytes = await bot.download_file(file.file_path)
    image_data = file_bytes.read()

    await state.update_data(image=image_data)
    await state.set_state(DesignFlow.waiting_for_description)

    await message.answer(
        "Фото получено! Теперь опиши желаемый дизайн:\n\n"
        "Например: *\"Гостиная в скандинавском стиле, светлые тона, дерево и белый цвет\"*",
        parse_mode="Markdown",
    )


@dp.message(DesignFlow.waiting_for_description)
async def handle_description_after_photo(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Пожалуйста, опиши желаемый дизайн текстом.")
        return

    data = await state.get_data()
    image_bytes = data.get("image")
    await state.clear()

    processing_msg = await message.answer("Генерирую дизайн... Это займёт около 30 секунд ⏳")

    try:
        result = await asyncio.to_thread(generate_interior, message.text, image_bytes)

        if result:
            await bot.delete_message(message.chat.id, processing_msg.message_id)
            await message.answer_photo(
                BufferedInputFile(result, filename="interior.jpg"),
                caption="Готово! Ваш дизайн интерьера 🏠",
            )
        else:
            await processing_msg.edit_text("Не удалось сгенерировать изображение. Попробуй ещё раз.")
    except Exception as e:
        logger.error(f"Generation error: {e}")
        try:
            await processing_msg.edit_text(f"Произошла ошибка. Попробуй ещё раз или напиши /start")
        except Exception:
            await message.answer("Произошла ошибка. Попробуй ещё раз или напиши /start")


@dp.message(F.text)
async def handle_text_only(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == DesignFlow.waiting_for_description.state:
        return

    processing_msg = await message.answer("Генерирую дизайн по описанию... ⏳")

    try:
        result = await asyncio.to_thread(generate_interior, message.text)

        if result:
            await bot.delete_message(message.chat.id, processing_msg.message_id)
            await message.answer_photo(
                BufferedInputFile(result, filename="interior.jpg"),
                caption="Готово! Ваш дизайн интерьера 🏠",
            )
        else:
            await processing_msg.edit_text("Не удалось сгенерировать изображение. Попробуй описать подробнее.")
    except Exception as e:
        logger.error(f"Generation error: {e}")
        try:
            await processing_msg.edit_text("Произошла ошибка. Попробуй ещё раз.")
        except Exception:
            await message.answer("Произошла ошибка. Попробуй ещё раз.")


async def main():
    logger.info("Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
