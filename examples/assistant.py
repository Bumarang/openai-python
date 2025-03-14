import openai

# gets API Key from environment variable OPENAI_API_KEY
client = openai.OpenAI()

assistant = client.beta.assistants.create(
    name="Huurrecht specialist",
    instructions="Je bent een huurrecht expert en geeft advies op grond van het woningwaarderingsstelsel",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4-1106-preview",
)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Ik wil de maximale huurprijs berekenen van een onzelfstandige woning 10m2 slaapkamer eigen wastafel gemeenschappelijke keuken en woonkamer 5 medebewoners gedeelde douche en wc fietsenberging en eigen balkon 3m2`. Kun je me helpen?",
)

run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="Please address the user as Mathijs Betten. The user has a premium account.",
)

print("Run completed with status: " + run.status)

if run.status == "completed":
    messages = client.beta.threads.messages.list(thread_id=thread.id)

    print("messages: ")
    for message in messages:
        assert message.content[0].type == "text"
        print({"role": message.role, "message": message.content[0].text.value})

    client.beta.assistants.delete(assistant.id)
