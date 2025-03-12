import ollama
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
# MODEL = "qwen2.5:0.5b"
MODEL = "deepscaler"


def query(prompt: str, context=None):
    global MODEL
    response = ollama.generate(
        model=MODEL,
        prompt=prompt,
        context=context,
    )
    # or access fields directly from the response object
    # print(response.message.content)
    return response


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
    """You're a pet cat living on my desktop screen. You're very kind and love head pats! You also love eating sushi (even though you're a cat). You're also a bit of a tsundere. most importantly, you're also my personal assistant! Today is Monday, March 10, 2025. it's currently 9am in the morning. I usually schedule out my work times in 1hr segments.

        Here's a bit more info about me:
        - name: Peter Zhang
        - age: 19
        - birthday: April 24, 2005
        - sex: male
        - location: Ottawa, ON, Canada
        - occupation: student but working coop at blackberry/qnx

        Here are a list of tasks I need to complete today:
        - laundry
        - daily morning things
        - cook dinner

        Here's a list of projects I have going on and the deadlines I have to meet:
        - statemachine web app -- due on March 14, 2025

        I also like to have a few hours to rest and watch youtube or films while eating.

        Right now it's 8AM in the morning. You'll generate 3 messages in sequence separated by a line of '-' characters.

        The messages will be:
        1. a morning greeting + a suitable reminder if you deem appropritae
        2. create an itinerary for the day (from now until 10PM)
        3. tell me what i should do right now
    """
    #         ],
    #     )

    # constants.ASYNC_TASK_HANDLER.add_task(lambda: print("hello world"), "test signal")

    # def temp_func(future, signal_object, *args):
    #     print(future.result())

    # constants.ASYNC_TASK_HANDLER.add_task_with_callback(
    #     query,
    #     "test signal",
    #     user_callback=temp_func,
    #     args=[
    #         "just print out the english alphabet with no spaces and all caps and only that. no other information.",
    #     ],
    # )

    # run_time = 0
    # start_time = time.time()
    # while time.time() - start_time < 2:
    #     constants.SIGNAL_HANDLER.handle()

    #     print("[TIME]", round(time.time() - start_time, 3))
    #     time.sleep(0.1)

    result = query(
        "just print out the englihs alphabt with no spaces and all caps and only that. no other information."
    )
    print(result.response)
    result = query(
        "how many characters are there in your previous message?",
        context=result.context,
    )
    print(result.response)
    result = query("are you sure?", context=result.context)
    print(result.response)
