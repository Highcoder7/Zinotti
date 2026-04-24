Nano Banana is the name for Gemini's native image generation capabilities. Gemini can generate and process images conversationally with text, images, or a combination of both. This lets you create, edit, and iterate on visuals with unprecedented control.

Nano Banana refers to three distinct models available in the Gemini API:

Nano Banana 2: The Gemini 3.1 Flash Image Preview model (gemini-3.1-flash-image-preview). This model serves as the high-efficiency counterpart to Gemini 3 Pro Image, optimized for speed and high-volume developer use cases.
Nano Banana Pro: The Gemini 3 Pro Image Preview model (gemini-3-pro-image-preview). This model is designed for professional asset production, utilizing advanced reasoning ("Thinking") to follow complex instructions and render high-fidelity text.
Nano Banana: The Gemini 2.5 Flash Image model (gemini-2.5-flash-image). This model is designed for speed and efficiency, optimized for high-volume, low-latency tasks.
All generated images include a SynthID watermark.

Image generation (text-to-image)
Python
JavaScript
Go
Java
REST

from google import genai
from google.genai import types
from PIL import Image

client = genai.Client()

prompt = ("Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme")
response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=[prompt],
)

for part in response.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        image = part.as_image()
        image.save("generated_image.png")
Image editing (text-and-image-to-image)
Reminder: Make sure you have the necessary rights to any images you upload. Don't generate content that infringe on others' rights, including videos or images that deceive, harass, or harm. Your use of this generative AI service is subject to our Prohibited Use Policy.

Provide an image and use text prompts to add, remove, or modify elements, change the style, or adjust the color grading.

The following example demonstrates uploading base64 encoded images. For multiple images, larger payloads, and supported MIME types, check the Image understanding page.

Python
JavaScript
Go
Java
REST

from google import genai
from google.genai import types
from PIL import Image

client = genai.Client()

prompt = (
    "Create a picture of my cat eating a nano-banana in a "
    "fancy restaurant under the Gemini constellation",
)

image = Image.open("/path/to/cat_image.png")

response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=[prompt, image],
)

for part in response.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        image = part.as_image()
        image.save("generated_image.png")
Multi-turn image editing
Keep generating and editing images conversationally. Chat or multi-turn conversation is the recommended way to iterate on images. The following example shows a prompt to generate an infographic about photosynthesis.

Python
Javascript
Go
Java
REST

from google import genai
from google.genai import types

client = genai.Client()

chat = client.chats.create(
    model="gemini-3.1-flash-image-preview",
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        tools=[{"google_search": {}}]
    )
)

message = "Create a vibrant infographic that explains photosynthesis as if it were a recipe for a plant's favorite food. Show the \"ingredients\" (sunlight, water, CO2) and the \"finished dish\" (sugar/energy). The style should be like a page from a colorful kids' cookbook, suitable for a 4th grader."

response = chat.send_message(message)

for part in response.parts:
    if part.text is not None:
        print(part.text)
    elif image:= part.as_image():
        image.save("photosynthesis.png")
AI-generated infographic about photosynthesis
AI-generated infographic about photosynthesis
You can then use the same chat to change the language on the graphic to Spanish.

Python
Javascript
Go
Java
REST

message = "Update this infographic to be in Spanish. Do not change any other elements of the image."
aspect_ratio = "16:9" # "1:1","1:4","1:8","2:3","3:2","3:4","4:1","4:3","4:5","5:4","8:1","9:16","16:9","21:9"
resolution = "2K" # "512", "1K", "2K", "4K"

response = chat.send_message(message,
    config=types.GenerateContentConfig(
        image_config=types.ImageConfig(
            aspect_ratio=aspect_ratio,
            image_size=resolution
        ),
    ))

for part in response.parts:
    if part.text is not None:
        print(part.text)
    elif image:= part.as_image():
        image.save("photosynthesis_spanish.png")
AI-generated infographic of photosynthesis in Spanish
AI-generated infographic of photosynthesis in Spanish
New with Gemini 3 Image models
Gemini 3 offers state-of-the-art image generation and editing models. Gemini 3.1 Flash Image is optimized for speed and high-volume use-cases, and Gemini 3 Pro Image is optimized for professional asset production. Designed to tackle the most challenging workflows through advanced reasoning, they excel at complex, multi-turn creation and modification tasks.

High-resolution output: Built-in generation capabilities for 1K, 2K, and 4K visuals.
Gemini 3.1 Flash Image adds the smaller 512 (0.5K) resolution.
Advanced text rendering: Capable of generating legible, stylized text for infographics, menus, diagrams, and marketing assets.
Grounding with Google Search: The model can use Google Search as a tool to verify facts and generate imagery based on real-time data (e.g., current weather maps, stock charts, recent events).
Gemini 3.1 Flash Image adds the integration of Grounding with Google Search for Images alongside Web Search.
Thinking mode: The model utilizes a "thinking" process to reason through complex prompts. It generates interim "thought images" (visible in the backend but not charged) to refine the composition before producing the final high-quality output.
Up to 14 reference images: You can now mix up to 14 reference images to produce the final image.
New aspect ratios: Gemini 3.1 Flash Image Preview adds 1:4, 4:1, 1:8, and 8:1 aspect ratios.
Use up to 14 reference images
Gemini 3 image models let you to mix up to 14 reference images. These 14 images can include the following:

Gemini 3.1 Flash Image Preview	Gemini 3 Pro Image Preview
Up to 10 images of objects with high-fidelity to include in the final image	Up to 6 images of objects with high-fidelity to include in the final image
Up to 4 images of characters to maintain character consistency	Up to 5 images of characters to maintain character consistency
Python
Javascript
Go
Java
REST

from google import genai
from google.genai import types
from PIL import Image

prompt = "An office group photo of these people, they are making funny faces."
aspect_ratio = "5:4" # "1:1","1:4","1:8","2:3","3:2","3:4","4:1","4:3","4:5","5:4","8:1","9:16","16:9","21:9"
resolution = "2K" # "512", "1K", "2K", "4K"

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=[
        prompt,
        Image.open('person1.png'),
        Image.open('person2.png'),
        Image.open('person3.png'),
        Image.open('person4.png'),
        Image.open('person5.png'),
    ],
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio=aspect_ratio,
            image_size=resolution
        ),
    )
)

for part in response.parts:
    if part.text is not None:
        print(part.text)
    elif image:= part.as_image():
        image.save("office.png")
AI-generated office group photo
AI-generated office group photo
Grounding with Google Search
Use the Google Search tool to generate images based on real-time information, such as weather forecasts, stock charts, or recent events.

Note that when using Grounding with Google Search with image generation, image-based search results are not passed to the generation model and are excluded from the response (see Grounding with Google Search for images)

Python
Javascript
Java
REST

from google import genai
prompt = "Visualize the current weather forecast for the next 5 days in San Francisco as a clean, modern weather chart. Add a visual on what I should wear each day"
aspect_ratio = "16:9" # "1:1","1:4","1:8","2:3","3:2","3:4","4:1","4:3","4:5","5:4","8:1","9:16","16:9","21:9"

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_modalities=['Text', 'Image'],
        image_config=types.ImageConfig(
            aspect_ratio=aspect_ratio,
        ),
        tools=[{"google_search": {}}]
    )
)

for part in response.parts:
    if part.text is not None:
        print(part.text)
    elif image:= part.as_image():
        image.save("weather.png")
AI-generated five day weather chart for San Francisco
AI-generated five day weather chart for San Francisco
The response includes groundingMetadata which contains the following required fields:

searchEntryPoint: Contains the HTML and CSS to render the required search suggestions.
groundingChunks: Returns the top 3 web sources used to ground the generated image
Grounding with Google Search for Images (3.1 Flash)
Note: This feature is only available for the Gemini 3.1 Flash Image model.
Grounding with Google Search for images allows models to use web images retrieved via Google Search as visual context for image generation. Image Search is a new search type within the existing Grounding with Google Search tool, functioning alongside standard Web Search.

To enable Image Search, configure the googleSearch tool in your API request and specify imageSearch within the searchTypes object. Image Search can be used independently or together with Web Search.

Note that Grounding with Google Search for images can't be used to search for people.

Python
JavaScript
Go
REST

from google import genai
prompt = "A detailed painting of a Timareta butterfly resting on a flower"

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        tools=[
            types.Tool(google_search=types.GoogleSearch(
                search_types=types.SearchTypes(
                    web_search=types.WebSearch(),
                    image_search=types.ImageSearch()
                )
            ))
        ]
    )
)

# Display grounding sources if available
if response.candidates and response.candidates[0].grounding_metadata and response.candidates[0].grounding_metadata.search_entry_point:
    display(HTML(response.candidates[0].grounding_metadata.search_entry_point.rendered_content))
Display requirements

When you use Image Search within Grounding with Google Search, you must comply with the following conditions:

Source attribution: You must provide a link to the webpage containing the source image (the "containing page," not the image file itself) in a manner that the user will recognize as a link.
Direct navigation: If you also choose to display the source images, you must provide a direct, single-click path from the source images to its containing source webpage. Any other implementation that delays or abstracts the end user's access to the source webpage, including but not limited to any multi-click path or the use of an intermediate image viewer, is not permitted.
Response

For grounded responses using image search, the API provides clear attribution and metadata to link its output to verified sources. Key fields in the groundingMetadata object include:

imageSearchQueries: The specific queries used by the model for visual context (image search).
groundingChunks: Contains source information for retrieved results. For image sources, these will be returned as redirect URLs using a new image chunk type. This chunk includes:

uri: The web page URL for attribution (the landing page).
image_uri: The direct image URL.
groundingSupports: Provides specific mappings that link the generated content to its relevant citation source in the chunks.

searchEntryPoint: Includes the "Google Search" chip containing compliant HTML and CSS to render Search Suggestions.

Generate images up to 4K resolution
Gemini 3 image models generate 1K images by default but can also output 2K, 4K, and 512 (0.5K) (Gemini 3.1 Flash Image only) images. To generate higher resolution assets, specify the image_size in the generation_config.

You must use an uppercase 'K' (e.g. 1K, 2K, 4K). The 512 value does not use a 'K' suffix. Lowercase parameters (e.g., 1k) will be rejected.

Python
Javascript
Go
Java
REST

from google import genai
from google.genai import types

prompt = "Da Vinci style anatomical sketch of a dissected Monarch butterfly. Detailed drawings of the head, wings, and legs on textured parchment with notes in English."
aspect_ratio = "1:1" # "1:1","1:4","1:8","2:3","3:2","3:4","4:1","4:3","4:5","5:4","8:1","9:16","16:9","21:9"
resolution = "1K" # "512", "1K", "2K", "4K"

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio=aspect_ratio,
            image_size=resolution
        ),
    )
)

for part in response.parts:
    if part.text is not None:
        print(part.text)
    elif image:= part.as_image():
        image.save("butterfly.png")
The following is an example image generated from this prompt:

AI-generated Da Vinci style anatomical sketch of a dissected Monarch butterfly.
AI-generated Da Vinci style anatomical sketch of a dissected Monarch butterfly.
Thinking Process
Gemini 3 image models are thinking models that use a reasoning process ("Thinking") for complex prompts. This feature is enabled by default and cannot be disabled in the API. To learn more about the thinking process, see the Gemini Thinking guide.

The model generates up to two interim images to test composition and logic. The last image within Thinking is also the final rendered image.

You can check the thoughts that lead to the final image being produced.

Python
Javascript

for part in response.parts:
    if part.thought:
        if part.text:
            print(part.text)
        elif image:= part.as_image():
            image.show()
Controlling thinking levels
With Gemini 3.1 Flash Image, you can control the amount of thinking the model uses to balance quality and latency. The default thinkingLevel is minimal, and the supported levels are minimal and high. Setting the thinkingLevel to minimal provides the lowest latency responses. Note that minimal thinking does not mean the model uses no thinking at all.

You can add the includeThoughts boolean to determine whether the model's generated thoughts are returned in the response, or remain hidden.

Python
JavaScript
Go
REST

from google import genai

response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents="A futuristic city built inside a giant glass bottle floating in space",
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        thinking_config=types.ThinkingConfig(
            thinking_level="High",
            include_thoughts=True
        ),
    )
)

for part in response.parts:
    if part.thought: # Skip outputting thoughts
      continue
    if part.text:
      display(Markdown(part.text))
    elif image:= part.as_image():
      image.show()
Note that thinking tokens are billed regardless of whether includeThoughts is set to true or false, as the thinking process always happens by default whether you view the process or not.

Thought Signatures
Thought signatures are encrypted representations of the model's internal thought process and are used to preserve reasoning context across multi-turn interactions. All responses include a thought_signature field. As a general rule, if you receive a thought signature in a model response, you should pass it back exactly as received when sending the conversation history in the next turn. Failure to circulate thought signatures may cause the response to fail. Check the thought signature documentation for more explanations of signatures overall.

Note: If you use the official Google Gen AI SDKs and use the chat feature (or append the full model response object directly to history), thought signatures are handled automatically. You do not need to manually extract or manage them, or change your code.
Here is how thought signatures work:

All inline_data parts with image mimetype which are part of the response should have signature.
If there are some text parts at the beginning (before any image) right after the thoughts, the first text part should also have a signature.
If inline_data parts with image mimetype are part of thoughts, they won't have signatures.
The following code shows an example of where thought signatures are included:


[
  {
    "inline_data": {
      "data": "<base64_image_data_0>",
      "mime_type": "image/png"
    },
    "thought": true // Thoughts don't have signatures
  },
  {
    "inline_data": {
      "data": "<base64_image_data_1>",
      "mime_type": "image/png"
    },
    "thought": true // Thoughts don't have signatures
  },
  {
    "inline_data": {
      "data": "<base64_image_data_2>",
      "mime_type": "image/png"
    },
    "thought": true // Thoughts don't have signatures
  },
  {
    "text": "Here is a step-by-step guide to baking macarons, presented in three separate images.\n\n### Step 1: Piping the Batter\n\nThe first step after making your macaron batter is to pipe it onto a baking sheet. This requires a steady hand to create uniform circles.\n\n",
    "thought_signature": "<Signature_A>" // The first non-thought part always has a signature
  },
  {
    "inline_data": {
      "data": "<base64_image_data_3>",
      "mime_type": "image/png"
    },
    "thought_signature": "<Signature_B>" // All image parts have a signatures
  },
  {
    "text": "\n\n### Step 2: Baking and Developing Feet\n\nOnce piped, the macarons are baked in the oven. A key sign of a successful bake is the development of \"feet\"—the ruffled edge at the base of each macaron shell.\n\n"
    // Follow-up text parts don't have signatures
  },
  {
    "inline_data": {
      "data": "<base64_image_data_4>",
      "mime_type": "image/png"
    },
    "thought_signature": "<Signature_C>" // All image parts have a signatures
  },
  {
    "text": "\n\n### Step 3: Assembling the Macaron\n\nThe final step is to pair the cooled macaron shells by size and sandwich them together with your desired filling, creating the classic macaron dessert.\n\n"
  },
  {
    "inline_data": {
      "data": "<base64_image_data_5>",
      "mime_type": "image/png"
    },
    "thought_signature": "<Signature_D>" // All image parts have a signatures
  }
]
Other image generation modes
Gemini supports other image interaction modes based on prompt structure and context, including:

Text to image(s) and text (interleaved): Outputs images with related text.
Example prompt: "Generate an illustrated recipe for a paella."
Image(s) and text to image(s) and text (interleaved): Uses input images and text to create new related images and text.
Example prompt: (With an image of a furnished room) "What other color sofas would work in my space? can you update the image?"
Generate images in batch
If you need to generate a lot of images, you can use the Batch API. You get higher rate limits in exchange for a turnaround of up to 24 hours.

Check the Batch API image generation documentation and the cookbook for Batch API image examples and code.

Prompting guide and strategies
Mastering image generation starts with one fundamental principle:

Describe the scene, don't just list keywords. The model's core strength is its deep language understanding. A narrative, descriptive paragraph will almost always produce a better, more coherent image than a list of disconnected words.

Prompts for generating images
The following strategies will help you create effective prompts to generate exactly the images you're looking for.

Photography
For realistic images, use photography terms. Mention camera angles, lens types, lighting, and fine details to guide the model toward a realistic result.

Prompt	Generated output
A photo of a close-up portrait of an elderly Japanese ceramicist with deep, sun-etched wrinkles and a warm, knowing smile. He is carefully inspecting a freshly glazed tea bowl. The setting is his rustic, sun-drenched workshop. The scene is illuminated by soft, golden hour light streaming through a window, highlighting the fine texture of the clay. Captured with an 85mm portrait lens, resulting in a soft, blurred background (bokeh). The overall mood is serene and masterful. Vertical portrait orientation.	Elderly Japanese ceramicist
Stylized illustrations and stickers
To create stickers, icons, or assets, be explicit about the style and request a white background.

Note: The model does not support generating a transparent background.
Prompt	Generated output
A kawaii-style sticker of a happy red panda wearing a tiny bamboo hat. It's munching on a green bamboo leaf. The design features bold, clean outlines, simple cel-shading, and a vibrant color palette. The background must be white.	Kawaii red panda sticker
Accurate text in images
Gemini excels at rendering text. Be clear about the text, the font style (descriptively), and the overall design. Use Gemini 3 Pro Image Preview for professional asset production.

Prompt	Generated output
Create a modern, minimalist logo for a coffee shop called 'The Daily Grind'. The text should be in a clean, bold, sans-serif font. The color scheme is black and white. Put the logo in a circle. Use a coffee bean in a clever way.	Coffee shop logo
Product mockups and commercial photography
Perfect for creating clean, professional product shots for ecommerce, advertising, or branding.

Prompt	Generated output
A high-resolution, studio-lit product photograph of a minimalist ceramic coffee mug in matte black, presented on a polished concrete surface. The lighting is a three-point softbox setup designed to create soft, diffused highlights and eliminate harsh shadows. The camera angle is a slightly elevated 45-degree shot to showcase its clean lines. Ultra-realistic, with sharp focus on the steam rising from the coffee. Square image.	Ceramic coffee mug product shot
Minimalist and negative space design
Excellent for creating backgrounds for websites, presentations, or marketing materials where text will be overlaid.

Prompt	Generated output
A minimalist composition featuring a single, delicate red maple leaf positioned in the bottom-right of the frame. The background is a vast, empty off-white canvas, creating significant negative space for text. Soft, diffused lighting from the top left. Square image.	Minimalist design with red maple leaf
Sequential art (Comic panel / Storyboard)
Builds on character consistency and scene description to create panels for visual storytelling. For accuracy with text and storytelling ability, these prompts work best with Gemini 3 Pro and Gemini 3.1 Flash Image Preview.

Prompt	Generated output
Input image:

Man in white glasses
Input image
Prompt: Make a 3 panel comic in a gritty, noir art style with high-contrast black and white inks. Put the character in a humurous scene.

Gritty noir comic panel
Grounding with Google Search
Use Google Search to generate images based on recent or real-time information. This is useful for news, weather, and other time-sensitive topics.

Prompt	Generated output
Make a simple but stylish graphic of last night's Arsenal game in the Champion's League	Arsenal football score graphic
Prompts for editing images
These examples show how to provide images alongside your text prompts for editing, composition, and style transfer.

Adding and removing elements
Provide an image and describe your change. The model will match the original image's style, lighting, and perspective.

Prompt	Generated output
Input image:

A photorealistic picture of a fluffy ginger cat...
Input image
Prompt: Using the provided image of my cat, please add a small, knitted wizard hat on its head. Make it look like it's sitting comfortably and matches the soft lighting of the photo.

Cat with wizard hat
Inpainting (Semantic masking)
Conversationally define a "mask" to edit a specific part of an image while leaving the rest untouched.

Prompt	Generated output
Input image:

A wide shot of a modern, well-lit living room...
Input image
Prompt: Using the provided image of a living room, change only the blue sofa to be a vintage, brown leather chesterfield sofa. Keep the rest of the room, including the pillows on the sofa and the lighting, unchanged.

Living room with brown leather sofa
Style transfer
Provide an image and ask the model to recreate its content in a different artistic style.

Prompt	Generated output
Input image:

A photorealistic, high-resolution photograph of a busy city street...
Input image
Prompt: Transform the provided photograph of a modern city street at night into the artistic style of Vincent van Gogh's 'Starry Night'. Preserve the original composition of buildings and cars, but render all elements with swirling, impasto brushstrokes and a dramatic palette of deep blues and bright yellows.

City street in Starry Night style
Advanced composition: Combining multiple images
Provide multiple images as context to create a new, composite scene. This is perfect for product mockups or creative collages.

Prompt	Generated output
Input images:

A professionally shot photo of a blue floral summer dress...
Input 1: Dress
Full-body shot of a woman with her hair in a bun...
Input 2: Model
Prompt: Create a professional e-commerce fashion photo. Take the blue floral dress from the first image and let the woman from the second image wear it. Generate a realistic, full-body shot of the woman wearing the dress, with the lighting and shadows adjusted to match the outdoor environment.

Fashion e-commerce shot
High-fidelity detail preservation
To ensure critical details (like a face or logo) are preserved during an edit, describe them in great detail along with your edit request.

Prompt	Generated output
Input images:

A professional headshot of a woman with brown hair and blue eyes...
Input 1: Woman
A simple, modern logo with the letters 'G' and 'A'...
Input 2: Logo
Prompt: Take the first image of the woman with brown hair, blue eyes, and a neutral expression. Add the logo from the second image onto her black t-shirt. Ensure the woman's face and features remain completely unchanged. The logo should look like it's naturally printed on the fabric, following the folds of the shirt.

Woman with logo on t-shirt
Bring something to life
Upload a rough sketch or drawing and ask the model to refine it into a finished image.

Prompt	Generated output
Input image:

Sketch of a car
Rough sketch of a car
Prompt: Turn this rough pencil sketch of a futuristic car into a polished photo of the finished concept car in a showroom. Keep the sleek lines and low profile from the sketch but add metallic blue paint and neon rim lighting.

Polished photo of concept car
Character consistency: 360 view
You can generate 360-degree views of a character by iteratively prompting for different angles. For best results, include previously generated images in subsequent prompts to maintain consistency. For complex poses, include a reference image of the desired pose.

Prompt	Generated output
Input image:

Original input of a man in white glasses
Original image
Prompt: A studio portrait of this man against white, in profile looking right

Output of a man in white glasses looking right
Man in white glasses looking right
Output of a man in white glasses looking forward
Man in white glasses looking forward
Best Practices
To elevate your results from good to great, incorporate these professional strategies into your workflow.

Be Hyper-Specific: The more detail you provide, the more control you have. Instead of "fantasy armor," describe it: "ornate elven plate armor, etched with silver leaf patterns, with a high collar and pauldrons shaped like falcon wings."
Provide Context and Intent: Explain the purpose of the image. The model's understanding of context will influence the final output. For example, "Create a logo for a high-end, minimalist skincare brand" will yield better results than just "Create a logo."
Iterate and Refine: Don't expect a perfect image on the first try. Use the conversational nature of the model to make small changes. Follow up with prompts like, "That's great, but can you make the lighting a bit warmer?" or "Keep everything the same, but change the character's expression to be more serious."
Use Step-by-Step Instructions: For complex scenes with many elements, break your prompt into steps. "First, create a background of a serene, misty forest at dawn. Then, in the foreground, add a moss-covered ancient stone altar. Finally, place a single, glowing sword on top of the altar."
Use "Semantic Negative Prompts": Instead of saying "no cars," describe the desired scene positively: "an empty, deserted street with no signs of traffic."
Control the Camera: Use photographic and cinematic language to control the composition. Terms like wide-angle shot, macro shot, low-angle perspective.
Limitations
For best performance, use the following languages: EN, ar-EG, de-DE, es-MX, fr-FR, hi-IN, id-ID, it-IT, ja-JP, ko-KR, pt-BR, ru-RU, ua-UA, vi-VN, zh-CN.
Image generation does not support audio or video inputs.
The model won't always follow the exact number of image outputs that the user explicitly asks for.
gemini-2.5-flash-image works best with up to 3 images as input, while gemini-3-pro-image-preview supports 5 images with high fidelity, and up to 14 images in total. gemini-3.1-flash-image-preview supports character resemblance of up to 4 characters and the fidelity of up to 10 objects in a single workflow.
When generating text for an image, Gemini works best if you first generate the text and then ask for an image with the text.
gemini-3.1-flash-image-preview Grounding with Google Search does not support using real-world images of people from web search at this time.
All generated images include a SynthID watermark.
Optional configurations
You can optionally configure the response modalities and aspect ratio of the model's output in the config field of generate_content calls.

Output types
The model defaults to returning text and image responses (i.e. response_modalities=['Text', 'Image']). You can configure the response to return only images without text using response_modalities=['Image'].

Python
JavaScript
Go
Java
REST

response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=[prompt],
    config=types.GenerateContentConfig(
        response_modalities=['Image']
    )
)
Aspect ratios and image size
The model defaults to matching the output image size to that of your input image, or otherwise generates 1:1 squares. You can control the aspect ratio of the output image using the aspect_ratio field under image_config in the response request, shown here:

Python
JavaScript
Go
Java
REST

# For gemini-2.5-flash-image
response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[prompt],
    config=types.GenerateContentConfig(
        image_config=types.ImageConfig(
            aspect_ratio="16:9",
        )
    )
)

# For gemini-3.1-flash-image-preview and gemini-3-pro-image-preview
response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=[prompt],
    config=types.GenerateContentConfig(
        image_config=types.ImageConfig(
            aspect_ratio="16:9",
            image_size="2K",
        )
    )
)

The different ratios available and the size of the image generated are listed in the following tables:

3.1 Flash Image Preview
3 Pro Image Preview
Gemini 2.5 Flash Image
Aspect ratio	512 resolution	0.5K tokens	1K resolution	1K tokens	2K resolution	2K tokens	4K resolution	4K tokens
1:1	512x512	747	1024x1024	1120	2048x2048	1680	4096x4096	2520
1:4	256x1024	747	512x2048	1120	1024x4096	1680	2048x8192	2520
1:8	192x1536	747	384x3072	1120	768x6144	1680	1536x12288	2520
2:3	424x632	747	848x1264	1120	1696x2528	1680	3392x5056	2520
3:2	632x424	747	1264x848	1120	2528x1696	1680	5056x3392	2520
3:4	448x600	747	896x1200	1120	1792x2400	1680	3584x4800	2520
4:1	1024x256	747	2048x512	1120	4096x1024	1680	8192x2048	2520
4:3	600x448	747	1200x896	1120	2400x1792	1680	4800x3584	2520
4:5	464x576	747	928x1152	1120	1856x2304	1680	3712x4608	2520
5:4	576x464	747	1152x928	1120	2304x1856	1680	4608x3712	2520
8:1	1536x192	747	3072x384	1120	6144x768	1680	12288x1536	2520
9:16	384x688	747	768x1376	1120	1536x2752	1680	3072x5504	2520
16:9	688x384	747	1376x768	1120	2752x1536	1680	5504x3072	2520
21:9	792x168	747	1584x672	1120	3168x1344	1680	6336x2688	2520
Model selection
Choose the model best suited for your specific use case.

Gemini 3.1 Flash Image Preview (Nano Banana 2 Preview) should be your go-to image generation model, as the best all around performance and intelligence to cost and latency balance. Check the model pricing and capabilities page for more details.

Gemini 3 Pro Image Preview (Nano Banana Pro Preview) is designed for professional asset production and complex instructions. This model features real-world grounding using Google Search, a default "Thinking" process that refines composition prior to generation, and can generate images of up to 4K resolutions. Check the model pricing and capabilities page for more details.

Gemini 2.5 Flash Image (Nano Banana) is designed for speed and efficiency. This model is optimized for high-volume, low-latency tasks and generates images at 1024px resolution. Check the model pricing and capabilities page for more details.

When to use Imagen
In addition to using Gemini's built-in image generation capabilities, you can also access Imagen, our specialized image generation model, through the Gemini API.

Imagen 4 should be your go-to model when starting to generate images with Imagen. Choose Imagen 4 Ultra for advanced use-cases or when you need the best image quality (note that can only generate one image at a time).

What's next
Find more examples and code samples in the cookbook guide.
Check out the Veo guide to learn how to generate videos with the Gemini API.
To learn more about Gemini models, see Gemini models.