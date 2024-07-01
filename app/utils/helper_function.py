from langchain_core.prompts import PromptTemplate

def generate_pengamalan_prompt(translation: str = "Hello world", tafsir: str = "Hello world"):
    template = f"""
    Anda adalah seorang penasihat yang bisa memberikan pengarahan, cara pengamalan, dan sejenisnya.
    Berdasarkan terjemah Al-Quran berikut "{translation}"
    dan tafsir berikut "{tafsir}".
    Berikan nasihat bagaimana cara pengamalannya menurut Al-Quran dan Sunnah. Pastikan jawaban anda itu singkat, padat, jelas, dan dalam bentuk paragraf.
    """
    final_prompt = PromptTemplate.from_template(template)
    return final_prompt