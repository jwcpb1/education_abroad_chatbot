import customtkinter as ctk #imports fancier library version of tkinter, allowing for more customizable interface options
from tkinter import filedialog #used to generate and export a pdf copy of tkinter conversation
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import openai #imports openai library that will be used to access chatGPT
openai.api_key = "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"
#Above is openAI access key to give python permission to openAI account
from PIL import Image

# Appearance setup
ctk.set_appearance_mode("light") #sets the GUI initial theme to light
# Theme definitions
LIGHT_THEME = { #below is the description for our light theme. for each line, the name of the feature is accompanied by a code for color
   "bg": "#ffffff",#white background
   "frame": "#f2f2f2",#light grey for windows or frames
   "button": "#1a2a40",#navy blue for buttons
   "hover": "#3c6e91",#muted blue, to signify when user is hovering
   "text": "#000000", #black text
   "entry": "#f2f2f2"} #light gray for frame
DARK_THEME = {
   "bg": "#121212",#very dark grey background
   "frame": "#2d2d2d",#dark grey frame
   "button": "#3c6e91",#muted blue color for button (inverse of light theme)
   "hover": "#5596c2",#light blue for hovor
   "text": "#ffffff",#white text
   "entry": "#2d2d2d"}#dark grey entry
current_theme = LIGHT_THEME
#Bottom def comes from youtube video for most part with minor tweaks to prompt
def chatbot_response(user_input): #def command for how the chatbot responds
    try:
        prompt = (#establishes the isntructions for chatgpt)
            f"You are a friendly assistant helping CSUMB students with education abroad questions.  "
            f"Respond clearly, in 1–3 sentences, using a friendly, conversational tone. Stay relevant to initial inquiry, and do not add extra, unrelated information.\n"
            f"User: {user_input}\nOtterBot:")
        response = openai.ChatCompletion.create( #initiates chat based request
            model="gpt-4", #selects which model
            messages=[
                {"role": "system",  # establishes role
                 "content": "You are OtterBot, a friendly and concise education abroad assistant for CSUMB students."},
                # prompt instructions
                {"role": "user", "content": prompt} #users input question or comment
            ],
            max_tokens=150, temperature=0.7) #limits output, temperature is high to signify warm conversational tone
        return response['choices'][0]['message']['content'].strip() #extracts and cleans text response from GPT api call
    except Exception as e: #error handling check
        return f" OpenAI error: {e}" #let user know error occured

def send_message():
   user_text = entry.get().strip()
   if not user_text:
       return
   chat_area.insert("end", f"\n👤 You:\n{user_text}\n", "user")
   response = chatbot_response(user_text)
   chat_area.insert("end", f"\n🤖 OtterBot:\n{response}\n", "bot")
   chat_area.insert("end", "\n" + "-" * 60 + "\n")
   chat_area.yview("end")
   entry.delete(0, "end")

def clear_chat():
   chat_area.delete("1.0", "end")


def export_chat_to_pdf():
   file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
   if not file_path:
       return
   try:
       pdf = canvas.Canvas(file_path, pagesize=letter)
       textobject = pdf.beginText(40, 750)
       textobject.setFont("Helvetica", 10)
       lines = chat_area.get("1.0", "end").split("\n")
       for line in lines:
           if textobject.getY() < 40:
               pdf.drawText(textobject)
               pdf.showPage()
               textobject = pdf.beginText(40, 750)
               textobject.setFont("Helvetica", 10)
           textobject.textLine(line)
       pdf.drawText(textobject)
       pdf.save()
       chat_area.insert("end", "\n✅ Chat exported to PDF!\n\n")
   except Exception as e:
       chat_area.insert("end", f"\n❌ Failed to export chat: {e}\n\n")


def toggle_theme():
   global current_theme
   if current_theme == LIGHT_THEME:
       current_theme = DARK_THEME
       theme_btn.configure(text="Light Mode")
   else:
       current_theme = LIGHT_THEME
       theme_btn.configure(text="Dark Mode")
   apply_theme()


def apply_theme():
   window.configure(fg_color=current_theme["bg"])
   chat_area.configure(fg_color=current_theme["frame"], text_color=current_theme["text"])
   entry.configure(fg_color=current_theme["entry"], text_color=current_theme["text"])
   button_frame.configure(fg_color=current_theme["frame"])
   label.configure(text_color=current_theme["button"])

   for btn in button_widgets:
       btn.configure(fg_color=current_theme["button"], hover_color=current_theme["hover"], text_color="white")
   for btn in category_buttons:
       btn.configure(fg_color=current_theme["button"], hover_color=current_theme["hover"], text_color="white")

# GUI Setup
window = ctk.CTk()
window.title("OtterBot – CSUMB Education Abroad Assistant")
window.geometry("700x750")
window.configure(fg_color=current_theme["bg"])

# Containers
button_widgets = []
category_buttons = []

image_path = "new.png"
image = Image.open(image_path)
image = image.resize((400, 100))
photo = ctk.CTkImage(light_image=image, dark_image=image, size=(400, 100))

# Display image at the top
image_label = ctk.CTkLabel(window, image=photo, text="")  #creates label widget, fillable by an image or text, in this case =photo is defined above as image
image_label.pack(pady=(10, 10)) #displays label on GUI with padding on both axis

# Label
label = ctk.CTkLabel(window, text="How can we help you learn about education abroad?",
        font=("Arial", 14, "bold"), text_color=current_theme["button"])
label.pack()
# Chat area
chat_area = ctk.CTkTextbox(window, width=650, height=300, font=("Arial", 12),
             fg_color=current_theme["frame"], text_color=current_theme["text"])
chat_area.pack(pady=15)

# User entry box
entry = ctk.CTkEntry(window, width=400, font=("Arial", 12),
            fg_color=current_theme["entry"], text_color=current_theme["text"])
entry.pack(pady=10)
# Button Frame
button_frame = ctk.CTkFrame(window, fg_color=current_theme["frame"])
button_frame.pack(pady=10)

# Control Buttons
for text, cmd in [("Send", send_message), ("Clear Chat", clear_chat),
                ("Export as PDF", export_chat_to_pdf), ("Quit", window.quit)]:
   btn = ctk.CTkButton(button_frame, text=text, command=cmd, corner_radius=20, width=120,
                 fg_color=current_theme["button"], hover_color=current_theme["hover"], text_color="white")
   btn.grid(row=0, column=len(button_widgets), padx=5)
   button_widgets.append(btn)
# Theme Toggle Button
theme_btn = ctk.CTkButton(window, text="Dark Mode", command=toggle_theme, corner_radius=20, width=160,
          fg_color=current_theme["button"], hover_color=current_theme["hover"], text_color="white")
theme_btn.pack(pady=10)
button_widgets.append(theme_btn)
# Apply initial theme
apply_theme() #calls on a function created earlier, with theme library (light and dark)
window.mainloop() #starts GUI event loop, keeps running until manually closed
