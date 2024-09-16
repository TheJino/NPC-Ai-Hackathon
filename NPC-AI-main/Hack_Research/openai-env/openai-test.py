import os.path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()   # load environmental variables
client = OpenAI()

\
    ######################### Charcter and setting choice
    #choose npc 

    #story_choice = input("What setting would you like: Faerun(Dnd) Europe(Dracula)\n")
    #if story_choice == "Faerun":
    #        story = open("story.txt", "rt")
    #elif story_choice == "Europe":
    #        story = open("story2.txt", "rt")
story = open("story2.txt", "rt")

# send a query to chat gpt
completion = client.chat.completions.create(
    model="gpt-4",
        messages=[
            {"role": "system", "content": f"The player has been sent to the town where this story {story.read()} takes place to investigate disappearances"},  # prompt
            {"role": "user", "content": "Paint an opening scenario that has routes leading to dialouge with either Bob the farmer, Barbara the Butcher, Pablo the trader, or Billy an old friend"}  # player question
        ]
)

scenario = str(completion.choices[0].message)
print(scenario[scenario.find("content=")+9:scenario.find("role=")-3])

while(True):
    story = open("story2.txt", "rt")
    dialogue_choice = input("\nWho would you like to talk to: Bob Barbara Pablo Billy \n")
    if dialogue_choice == "Bob" or dialogue_choice == "bob" :
        npc_params = open("NPC1.txt", "rt")
        npc = "Bob:"
    elif dialogue_choice == "Barbara" or dialogue_choice == "barbara" :
        npc_params = open("NPC2.txt", "rt")
        npc = "Barbara:"
    elif dialogue_choice == "Pablo" or dialogue_choice == "pablo" :
        npc_params = open("NPC3.txt", "rt")
        npc = "Pablo:"
    elif dialogue_choice == "Billy" or dialogue_choice == "billy" :
        npc_params = open("NPC4.txt", "rt")
        npc = "Billy:"



    def talk_to_npc(user_input, conversation_history):  # user input and string of convo hist
        # start the conversation history
        conversation_history += f"Player: {user_input}\n"

        # send a query to chat gpt
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"You are a this person {npc_params.read()} in this story {story.read()}"},  # prompt
                {"role": "user", "content": conversation_history}  # player question
            ]
        )

        # receive the generated response
        npc_response = completion.choices[0].message

        # add generated response to the chat history
        test = str(npc_response)
        test = test[test.find(npc):test.find("role=")-3]
        conversation_history += f"{test}\n"

        return npc_response, conversation_history



    # Initialize conversation history
    conversation_history = ""

    while True:
        print("Type quit to leave conversation")
        # Receive user input
        user_input = input("Player: ")

        if user_input == "quit":
            break

        # store npc_respinse, and convo history
        npc_response, conversation_history = talk_to_npc(user_input, conversation_history)

        # Print only the NPC response
   

        test = str(npc_response)
        print(test[test.find(npc):test.find("role=")-3])

    # Extract and save only the NPC responses to NPC1.txt
    if dialogue_choice == "Bob" or dialogue_choice == "bob" :
        npc_params = open("NPC1.txt", "a")
    elif dialogue_choice == "Barbara" or dialogue_choice == "barbara" :
        npc_params = open("NPC2.txt", "a")
    elif dialogue_choice == "Pablo" or dialogue_choice == "pablo" :
        npc_params = open("NPC3.txt", "a")
    elif dialogue_choice == "Billy" or dialogue_choice == "billy" :
        npc_params = open("NPC4.txt", "a")
    npc_params.write(conversation_history)


    #leave game
    main_quit = input("Quit(Y/N): ")
    if main_quit == "Y" or main_quit == "y":
        npc_params.close()
        story.close()
        break
        
    completion = client.chat.completions.create(
    model="gpt-4",
        messages=[
            {"role": "system", "content": f"The player has just finsied talking with {dialogue_choice} with the new info {conversation_history} and context of the story {story.read()}"},  # prompt
            {"role": "user", "content": "create a new scenario with the npc's that leads into new dialogue with the npc's or another openended path and ends the day for the player. opening the next day for continued dialouge with either Bob, Barbara, Pablo, or Billy"}  # player question
        ]
    )
    scenario = str(completion.choices[0].message)
    print(scenario[scenario.find("content=")+9:scenario.find("role=")-3])
    story =  open("story2.txt", "a")
    story.write(scenario[scenario.find("content=")+9:scenario.find("role=")-3])