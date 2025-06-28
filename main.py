import os
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from dotenv import load_dotenv
import chainlit as cl

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")


external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client = external_client
)

config = RunConfig(
    model = model,
    model_provider = external_client,
    tracing_disabled = True
)

agent : Agent= Agent(name="assistant", instructions="ahelpful asssistant", model=model)

@cl.on_message
async def handle_message(message: cl.Message):
    result = await Runner.run(
        agent,
        input=message.content,
        run_config=config
    )
    await cl.Message(content=result.final_output).send()

@cl.on_chat_start
async def start():
    await cl.Message(content=" Welcome to Muhammad Anas helping bot").send()

