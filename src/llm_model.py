import locale
from unsloth import FastLanguageModel

# Set locale encoding
locale.getpreferredencoding = lambda: "UTF-8"

# Load Unsloth Llama 3.1 3B model with 4-bit quantization for 12GB VRAM
model_name = "unsloth/Llama-3.2-3B-Instruct-bnb-4bit"
max_seq_length = 50000
dtype = None
load_in_4bit = True

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=model_name,
    max_seq_length=max_seq_length,
    dtype=dtype,
    load_in_4bit=load_in_4bit,
    device_map="auto",  # Automatically use GPU
)

# Enable native 2x faster inference
FastLanguageModel.for_inference(model)


def llm_model(prompttemplate, dbschema, input_query):
    """
    Process query translation using Unsloth model directly.
    
    Args:
        prompttemplate: Prompt template string with {database_info} and {user_query} placeholders
        dbschema: Database schema information
        input_query: User's natural language query
        
    Returns:
        dict: Result containing the generated query (compatible with LangChain format)
    """
    try:
        # Format the prompt template by replacing placeholders
        formatted_prompt = prompttemplate.format(
            database_info=dbschema,
            user_query=input_query
        )
        
        # Tokenize the input
        inputs = tokenizer(
            [formatted_prompt],
            return_tensors="pt"
        ).to("cuda")
        
        # Generate response
        outputs = model.generate(
            **inputs,
            max_new_tokens=1800,
            temperature=0,
            do_sample=False,
        )
        
        # Decode the generated text
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract only the generated part (remove the input prompt)
        # The model generates the full text including the prompt, so we extract the response part
        if "[/INST]" in generated_text:
            # Extract text after [/INST] tag
            response = generated_text.split("[/INST]")[-1].strip()
        else:
            # If no [/INST] tag, use the generated text as-is
            response = generated_text.replace(formatted_prompt, "").strip()
        
        # Return in format compatible with LangChain (dict with 'text' key)
        return {"text": response}
        
    except Exception as e:
        raise Exception(f"Error generating query: {str(e)}")
