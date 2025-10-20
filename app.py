import gradio as gr
import time
import logging
from cognitive_engine import aventro_ai

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def chat_interface(message, history):
    """Main chat function for Gradio"""
    try:
        start_time = time.time()
        
        # Get AI response
        response_data = aventro_ai.generate_cognitive_response(message)
        response_text = response_data["response"]
        
        processing_time = time.time() - start_time
        logger.info(f"Response generated in {processing_time:.2f}s")
        
        # Add subtle typing effect
        time.sleep(0.3)
        
        return response_text
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return "I apologize, but I encountered an error. Please try again."

def clear_memory():
    """Clear conversation memory"""
    aventro_ai.conversation_memory.clear()
    return "Conversation memory cleared!"

# Create the Gradio interface
with gr.Blocks(theme=gr.themes.Soft(), title="Aventro AI Hosting Assistant") as demo:
    gr.Markdown(
        """
        # 🚀 Aventro AI Hosting Assistant
        **Your intelligent managed hosting consultant**
        
        *Powered by advanced AI with cognitive behaviors*
        """
    )
    
    with gr.Row():
        chatbot = gr.Chatbot(
            label="Aventro AI Conversation",
            height=500,
            show_copy_button=True,
            placeholder="Ask me about hosting plans, pricing, or technical support..."
        )
    
    with gr.Row():
        msg = gr.Textbox(
            label="Your message",
            placeholder="Type your question here...",
            scale=4,
            lines=1,
            max_lines=3
        )
        submit_btn = gr.Button("Send 🚀", variant="primary", scale=1)
    
    with gr.Row():
        gr.Markdown("### Quick Actions")
    
    with gr.Row():
        gr.Button("View Plans", size="sm").click(
            fn=lambda: "What hosting plans do you offer?",
            outputs=msg
        )
        gr.Button("Get Support", size="sm").click(
            fn=lambda: "I need technical support",
            outputs=msg
        )
        gr.Button("See Pricing", size="sm").click(
            fn=lambda: "How much does it cost?",
            outputs=msg
        )
        gr.Button("Clear Chat", size="sm", variant="secondary").click(
            fn=lambda: None,
            outputs=chatbot
        )
    
    with gr.Row():
        gr.Markdown("### Examples to try:")
        gr.Examples(
            examples=[
                "What hosting plans do you offer?",
                "I need help with website migration",
                "How much does the Business plan cost?",
                "Do you offer email hosting?",
                "What's included in your support?"
            ],
            inputs=msg,
            label="Try these questions:"
        )
    
    # Event handlers
    def respond(message, chat_history):
        bot_response = chat_interface(message, chat_history)
        chat_history.append((message, bot_response))
        return "", chat_history
    
    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    submit_btn.click(respond, [msg, chatbot], [msg, chatbot])

# For Hugging Face Spaces
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True  # Creates public link
    )
