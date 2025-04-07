# build the ollama image for the assistant
ollama create Assistant_Pet -f assets/assistant_modelfile

# run the ollama image
ollama run Assistant_Pet

