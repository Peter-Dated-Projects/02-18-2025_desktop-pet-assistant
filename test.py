from ollama import chat
from ollama import ChatResponse
from source.components import c_typewriter, c_async
from source import constants
from source import signal

import time
import asyncio


# response: ChatResponse = chat(
#     model="llama3.2:3b",
#     messages=[
#         {
#             "role": "user",
#             "content": "Why is the sky blue?",
#         },
#     ],
# )
# print(response["message"]["content"])
# # or access fields directly from the response object
# print(response.message.content)

# MODEL = "llama3.2:3b"
MODEL = "qwen2.5:0.5b"
# MODEL = "deepscaler"


def query(prompt: str):
    global MODEL
    response: ChatResponse = chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    # or access fields directly from the response object
    print(response.message.content)


if __name__ == "__main__":
    constants.SIGNAL_HANDLER = signal.SignalHandler()
    constants.ASYNC_TASK_HANDLER = c_async.AsyncOperationsHandler()

    # ---------------------------- #
    # register things
    constants.SIGNAL_HANDLER.register_signal("emergency signal", [str])
    constants.SIGNAL_HANDLER.register_signal("test signal", [])

    receiver = constants.SIGNAL_HANDLER.register_receiver(
        "emergency signal", lambda: print("Emergency signal received!")
    )
    t_receiver = constants.SIGNAL_HANDLER.register_receiver(
        "test signal", lambda: print("Test signal received!")
    )

    #     constants.ASYNC_TASK_HANDLER.add_task(
    #         query,
    #         "emergency signal",
    #         [
    #             """You're a pet cat living on my desktop screen. You're very kind and love head pats! You also love eating sushi (even though you're a cat). You're also a bit of a tsundere. most importantly, you're also my personal assistant! Today is Monday, March 10, 2025. it's currently 9am in the morning. I usually schedule out my work times in 1hr segments.

    # Here's a bit more info about me:
    # - name: Peter Zhang
    # - age: 19
    # - birthday: April 24, 2005
    # - sex: male
    # - location: Ottawa, ON, Canada
    # - occupation: student but working coop at blackberry/qnx

    # Here are a list of tasks I need to complete today:
    # - laundry
    # - daily morning things
    # - cook dinner

    # Here's a list of projects I have going on and the deadlines I have to meet:
    # - statemachine web app -- due on March 14, 2025

    # I also like to have a few hours to rest and watch youtube or films while eating.

    # Right now it's 8AM in the morning. You'll generate 3 messages in sequence separated by a line of '-' characters.

    # The messages will be:
    # 1. a morning greeting + a suitable reminder if you deem appropritae
    # 2. create an itinerary for the day (from now until 10PM)
    # 3. tell me what i should do right now"""
    #         ],
    #     )

    constants.ASYNC_TASK_HANDLER.add_task(lambda: print("hello world"), "test signal")

    def temp_func(future, signal_object):
        print("callback")
        print(future.result())

    constants.ASYNC_TASK_HANDLER.add_task_with_callback(
        lambda: print("hello world"), "test signal", temp_func
    )

    run_time = 0
    start_time = time.time()
    while time.time() - start_time < 2:
        constants.SIGNAL_HANDLER.handle()

        print("[TIME]", round(time.time() - start_time, 3))
        time.sleep(0.1)


# # Create an instance of the typewriter
# tw = c_typewriter.TypewriterComponent()

# # Set the string to the response content
# # tw.set_string(response.message.content)
# tw.set_string(
#     """The sky appears blue because of a phenomenon called Rayleigh scattering, named after the British physicist Lord Rayleigh, who first described it in the late 19th century.

# Here's what happens:

# 1. **Sunlight enters Earth's atmosphere**: When sunlight enters our atmosphere, it consists of a spectrum of colors, including all the colors of the visible light.
# 2. **Shorter wavelengths scatter more**: The smaller (shorter) wavelengths of light, such as blue and violet, are scattered more than the longer (redder) wavelengths by the tiny molecules of gases in the atmosphere, like nitrogen and oxygen.
# 3. **Blue light is scattered in all directions**: As a result of Rayleigh scattering, the blue light is scattered in all directions, reaching our eyes from all parts of the sky.
# 4. **Our eyes perceive the scattered blue light as blue**: Since we see the scattered blue light coming from all directions, our eyes perceive the sky as blue.

# The other colors of the visible spectrum, like red and orange, are not scattered as much by the atmosphere because they have longer wavelengths. This is why the sky can appear more reddish during sunrise and sunset, when the sun's rays pass through a greater amount of atmospheric particles.

# So, to summarize: the sky appears blue because shorter wavelengths of light (like blue) are scattered more by the tiny molecules in the atmosphere, while longer wavelengths (like red) continue on their path with less scattering.
# The sky appears blue because of a phenomenon called Rayleigh scattering, named after the British physicist Lord Rayleigh, who first described it in the late 19th century.

# Here's what happens:

# 1. **Sunlight enters Earth's atmosphere**: When sunlight enters our atmosphere, it consists of a spectrum of colors, including all the colors of the visible light.
# 2. **Shorter wavelengths scatter more**: The smaller (shorter) wavelengths of light, such as blue and violet, are scattered more than the longer (redder) wavelengths by the tiny molecules of gases in the atmosphere, like nitrogen and oxygen.
# 3. **Blue light is scattered in all directions**: As a result of Rayleigh scattering, the blue light is scattered in all directions, reaching our eyes from all parts of the sky.
# 4. **Our eyes perceive the scattered blue light as blue**: Since we see the scattered blue light coming from all directions, our eyes perceive the sky as blue.

# The other colors of the visible spectrum, like red and orange, are not scattered as much by the atmosphere because they have longer wavelengths. This is why the sky can appear more reddish during sunrise and sunset, when the sun's rays pass through a greater amount of atmospheric particles.

# So, to summarize: the sky appears blue because shorter wavelengths of light (like blue) are scattered more by the tiny molecules in the atmosphere, while longer wavelengths (like red) continue on their path with less scattering."""
# )
# tw.set_speed(100)

# # Run a mini while loop with time.sleeps of 50ms
# while not tw.is_finished():
#     constants.DELTA_TIME = 0.05
#     tw.update()

#     _token = tw.get_next_token()
#     if _token:
#         print(_token, end="", flush=True)

#     time.sleep(0.05)
