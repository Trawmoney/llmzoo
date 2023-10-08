import streamlit as st
import threading
import os
import litellm
from litellm import completion
from dotenv import load_dotenv

# load .env, so litellm reads from .env
load_dotenv()

litellm.token = "5fdb5efa-9307-40ed-b824-1c73a1613030"

models = []
provider_models_map  = litellm.models_by_provider
for provider in provider_models_map:
    print(provider)
    for model in provider_models_map[provider]:
        print(provider_models_map[provider])
        models.append(provider+"/" + model)

# Function to get model outputs
def get_model_output(prompt, model_name):
    try:
        messages = [
            {"role": "user", "content": prompt},
        ]
        response = completion(messages=messages, model=model_name)
        
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"got error calling LLM API {e}"

# Function to get model outputs
def get_model_output_thread(prompt, model_name, outputs, idx):
    output = get_model_output(prompt, model_name)
    outputs[idx] = output

# Streamlit app
def main():
    keys = {}
    st.title("LiteLLM Playground")
    st.markdown("[LiteLLM - one package for CodeLlama, Llama2 Anthropic, Cohere, OpenAI, Replicate](https://github.com/BerriAI/litellm/)")
    st.markdown("View Request Logs + Manage keys (Optional) [here:](https://admin.litellm.ai/5fdb5efa-9307-40ed-b824-1c73a1613030)")

    # Sidebar for user input
    with st.sidebar:
        st.header("User Settings")
            # List of models to test
        model_names = models # Add your model names here

        # Dropdowns for model selection
        selected_models = []
        for i in range(4):
            selected_model = st.selectbox(f"Select Model {i+1}", model_names, index=i)
            selected_models.append(selected_model)
                
            provider = selected_model.split("/")[0]
            key_name = f"{provider.upper()}_API_KEY"
            api_key = st.text_input(f"Enter your {key_name}", type="password", key=i)
            keys[key_name] = api_key
        set_keys_button = st.button("Set API Keys")
    
    if set_keys_button:
        for key in keys:
            if os.environ.get(key) != None: # if key not set in .env
                os.environ[key] = keys[key]
        st.success("API keys have been set.")

    st.header("User Input")
    prompt = st.text_area("Enter your prompt here:")
    submit_button = st.button("Submit")

    # Main content area to display model outputs
    st.header("Model Outputs")
    
    cols = st.columns(len(selected_models))  # Create columns
    outputs = [""] * len(selected_models)  # Initialize outputs list with empty strings

    threads = []
    if submit_button and prompt:
        for idx, model_name in enumerate(selected_models):
            thread = threading.Thread(target=get_model_output_thread, args=(prompt, model_name, outputs, idx))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    # Display text areas and fill with outputs if available
    for idx, model_name in enumerate(selected_models):
        with cols[idx]:
            st.text_area(label=f"{model_name}", value=outputs[idx], height=300, key=f"output_{model_name}_{idx}")  # Use a unique key

if __name__ == "__main__":
    main()
