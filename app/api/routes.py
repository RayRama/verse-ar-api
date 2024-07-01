import json
import os, requests
from . import api_blueprint
from flask import request, jsonify
# from app.services.openai_service import generate_question_jobdesc
from app.services.cohere_service import generate_pengamalan

KEMENAG_URL = os.getenv('KEMENAG_API')
QURAN_URL = os.getenv('QURAN_API')

@api_blueprint.route('/api/test', methods=['GET'])
def test():
    return jsonify({"response": "Hello World"})


@api_blueprint.route('/api/list-ayah-by-page', methods=['GET'])
def list_ayah_by_page():
    page = request.args.get('page')

    if page is None:
        return jsonify({"error": "Page is required"}), 400

    try:
        page = int(page)
    except ValueError:
        return jsonify({"error": "Invalid page number"}), 400

    if page > 604:
        return jsonify({"error": "Page not found"}), 404

    try:
        response = requests.get(f"{QURAN_URL}/verses/by_page/{page}?language=id&translations=33")
        response.raise_for_status()
        ayah_list = response.json().get('verses')
    except requests.RequestException:
        return jsonify({"error": "Failed to retrieve ayahs"}), 500

    surah_number = ayah_list[0].get('verse_key').split(':')[0]

    try:
        response = requests.get(f"{QURAN_URL}/chapters/{surah_number}")
        response.raise_for_status()
        chapter_info = response.json().get('chapter')
    except requests.RequestException:
        return jsonify({"error": "Failed to retrieve chapter information"}), 500

    result = {
        "message": "Success",
        "surah": chapter_info.get('name_simple'),
        "ayah": [
            {
                "id": ayah.get('id'),
                "verse_number": ayah.get('verse_number')
            } for ayah in ayah_list
        ]
    }

    return jsonify(result)

@api_blueprint.route('/api/detail-ayah', methods=['GET'])
def detail_ayah():
    verse_id = request.args.get('id')

    if verse_id is None:
        return jsonify({"error": "Verse ID is required"}), 400

    try:
        response = requests.get(f"{KEMENAG_URL}/quran-tafsir/{verse_id}")
        response.raise_for_status()
    except requests.RequestException:
        return jsonify({"error": "Failed to retrieve ayah"}), 500

    ayah = response.json().get('data')

    result = {
        "message": "Success",
        "ayah": {
            "id": ayah.get('id'),
            "ayah": ayah.get('arabic'),
            "translation": ayah.get('translation'),
            "tafsir": ayah.get('tafsir').get('wajiz')
        }
    }

    return jsonify(result)

@api_blueprint.route('/api/generate-pengamalan', methods=['POST'])
def generate_pengamalan_by_ayah():
    data = request.json

    translation = data.get('translation')
    tafsir = data.get('tafsir')

    if translation is None and tafsir is None:
        return jsonify({"error": "Terjemah and Tafsir are required"}), 400

    generated_pengamalan = generate_pengamalan(translation, tafsir)

    result = {
        "message": "Success",
        "generated_pengamalan": generated_pengamalan.content
    }

    return jsonify(result)

# @api_blueprint.route('/api/list-ayah-by-page', methods=['GET'])
# def list_ayah_by_page():
#
#     page = request.args.get('page')
#
#     page = int(page)
#
#     if page is None:
#         return jsonify({"error": "Page is required"}), 400
#
#     if page > 604:
#         return jsonify({"error": "Page not found"}), 404
#
#     by_page = f"{QURAN_URL}/verses/by_page/{page}?language=id&translations=33"
#
#     by_page_response = requests.get(by_page)
#
#     list_ayah = by_page_response.json().get('verses')
#
#     surah = list_ayah[0].get('verse_key').split(':')[0]
#
#     by_chapter = f"{QURAN_URL}/chapters/{surah}"
#
#     by_chapter_response = requests.get(by_chapter)
#
#     chapter = by_chapter_response.json().get('chapter')
#
#     # start = int(list_ayah[0].get('verse_key').split(':')[1]) - 1
#     #
#     # end = int(list_ayah[-1].get('verse_key').split(':')[1])
#     #
#     # by_kemenag = f"{KEMENAG_URL}/quran-ayah?surah={surah}&start={start}&limit={end}"
#     #
#     # kemenag_response = requests.get(by_kemenag)
#     #
#     # kemenag_ayah = kemenag_response.json().get('data')
#
#     final_result = dict({
#         "message": "Success",
#         "surah": chapter.get('name_simple'),
#         "ayah": [{
#             "id": ayah.get('id'),
#             "verse_number": ayah.get('verse_number'),
#         } for ayah in list_ayah]
#     })
#
#     return jsonify(final_result)