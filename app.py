from shiny import App, render, ui, reactive
import shinyswatch
import os
import openai
import asyncio
import time
from dotenv import load_dotenv

load_dotenv(".env")

openai.api_key = os.environ.get("OPENAI_API_KEY")

messages = [
    {"role": "system", "content": "You are a helpful and kind AI Assistant."},
]

def chatbot(input):
  if input:
    messages.append({"role": "user", "content": input})
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=messages
    )
    reply = chat.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    return reply


app_ui = ui.page_fluid(
   ui.page_navbar(
        shinyswatch.theme.vapor(),
        ui.nav(
            ui.input_text_area("text_input", "Ask a Question!"),
            ui.input_action_button("submit","Submit"),
            ui.output_text_verbatim("text_output")
        )
   )
)


def server(input, output, session):
    @output
    @render.text
    @reactive.event(input.submit)
    async def text_output():
        with ui.Progress(min=1, max=20) as p:
            p.set(message="Getting answer", detail="This may take a while...")

            for i in range(1, 50):
                p.set(i, message="Getting answer")
                await asyncio.sleep(1)


        output = chatbot(input.text_input())
        return output


app = App(app_ui, server)
