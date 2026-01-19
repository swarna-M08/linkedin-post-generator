import os
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

# ১. .env লোড করা
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

print("---------------- AUTO-FIX TEST START ----------------")

if not GOOGLE_API_KEY:
    print("❌ ERROR: API Key পাওয়া যায়নি! .env ফাইল চেক করুন।")
else:
    print(f"✅ API Key Found: {GOOGLE_API_KEY[:5]}...")

    # ২. Google-কে জিজ্ঞাসা করা হচ্ছে কোন মডেলটি অ্যাভেলেবল
    genai.configure(api_key=GOOGLE_API_KEY)
    valid_model_name = None
    
    print("\n🔍 আপনার চাবির জন্য সঠিক মডেল খোঁজা হচ্ছে...")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                # সাধারণত models/gemini-1.5-flash বা models/gemini-pro পাওয়া যায়
                if "gemini" in m.name:
                    valid_model_name = m.name.replace("models/", "") # models/ অংশটি কেটে ফেলা হলো
                    print(f"✅ সঠিক মডেল পাওয়া গেছে: {valid_model_name}")
                    break
        
        if not valid_model_name:
            # যদি কিছু না পাওয়া যায়, ডিফল্ট হিসেবে এটা সেট হবে
            print("⚠️ অটোমেটিক পাওয়া যায়নি, ডিফল্ট 'gemini-1.5-flash' ব্যবহার করা হচ্ছে।")
            valid_model_name = "gemini-1.5-flash"

        # ৩. LangChain সেটআপ (পাওয়া মডেলটি দিয়ে)
        llm = ChatGoogleGenerativeAI(
            model=valid_model_name,
            google_api_key=GOOGLE_API_KEY
        )

        prompt = PromptTemplate(
            input_variables=["topic"],
            template="Write a 2-line LinkedIn post about {topic}."
        )

        chain = prompt | llm | StrOutputParser()

        # ৪. জেনারেট টেস্ট
        print(f"\n🚀 '{valid_model_name}' দিয়ে পোস্ট জেনারেট করার চেষ্টা চলছে...")
        result = chain.invoke({"topic": "Coding"})
        
        print("\n🎉 SUCCESS! জেনারেট হওয়া পোস্ট:")
        print("-----------------------------------")
        print(result)
        print("-----------------------------------")

    except Exception as e:
        print("\n❌ FAILED. আসল কারণ:")
        print(e)

print("---------------- TEST END ----------------")