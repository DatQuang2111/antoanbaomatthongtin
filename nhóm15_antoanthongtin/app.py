import os
import json
from flask import Flask, render_template, request, jsonify
from crypto_utils import CryptoUtils

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "treasure-hunt-secret-key-2024")

# Game data - Vietnamese cryptography puzzles với nhiều levels đa dạng
PUZZLES = [
    # Caesar Cipher Levels
    {
        "id": 1,
        "level": 1,
        "algorithm": "Caesar",
        "title": "Cuộn Cổ Bí Ẩn",
        "description": "Thám tử Smith tìm thấy một cuộn giấy cổ với thông điệp được mã hóa bằng mật mã Caesar. Đây là manh mối đầu tiên dẫn đến kho báu.",
        "story": "Trong một căn phòng cổ kính, Smith phát hiện ra cuộn giấy bị ẩn sau bức tranh. Thông điệp được viết bằng mật mã Caesar cổ điển.",
        "ciphertext": "WKDP WX VPLWK GD WLP WKDR NKR EDX WKDW WX",
        "correct_key": "3",
        "plaintext": "THAM TU SMITH DA TIM THAY KHO BAU THAT TU",
        "hint_1": "Mật mã Caesar dịch chuyển các chữ cái trong bảng chữ cái.",
        "hint_2": "Thử với số dịch chuyển nhỏ, từ 1 đến 10.",
        "hint_3": "Khóa là số 3 - dịch chuyển mỗi chữ cái 3 vị trí.",
        "points": 100,
        "difficulty": "Dễ"
    },
    # Vigenère Cipher Level
    {
        "id": 2,
        "level": 2,
        "algorithm": "Vigenère",
        "title": "Nhật Ký Thám Tử",
        "description": "Trong văn phòng cũ, Smith tìm thấy nhật ký của một thám tử trước đây với mật mã Vigenère phức tạp hơn.",
        "story": "Cuốn nhật ký cũ kỹ chứa đựng bí mật của những thám tử trước đây. Mật mã Vigenère yêu cầu một từ khóa đặc biệt.",
        "ciphertext": "NGIY LEI SHUBG TA SE TIM THIY KHO BIU",
        "correct_key": "DETECTIVE",
        "plaintext": "NGAY MAI CHUNG TA SE TIM THAY KHO BAU",
        "hint_1": "Mật mã Vigenère sử dụng một từ khóa để mã hóa.",
        "hint_2": "Từ khóa liên quan đến nghề nghiệp của Smith.",
        "hint_3": "Thử từ khóa 'DETECTIVE' - nghề nghiệp thám tử.",
        "points": 200,
        "difficulty": "Trung bình"
    },
    # Caesar Cipher Level (khác shift)
    {
        "id": 3,
        "level": 3,
        "algorithm": "Caesar",
        "title": "Bức Thư Cổ",
        "description": "Smith tìm thấy bức thư trong hòm cổ, được mã hóa bằng Caesar với độ dịch chuyển khác.",
        "story": "Bức thư được viết trên giấy cổ, mực đã phai nhạt theo thời gian. Độ dịch chuyển lần này có vẻ khác so với lần trước.",
        "ciphertext": "AOLY PZ H ULLK MVY ZLJYLA JOVK",
        "correct_key": "7",
        "plaintext": "THIS IS A NEED FOR SECRET CODE",
        "hint_1": "Mật mã Caesar với độ dịch chuyển lớn hơn lần trước.",
        "hint_2": "Thử các số từ 5 đến 10.",
        "hint_3": "Khóa là số 7 - dịch chuyển 7 vị trí.",
        "points": 150,
        "difficulty": "Dễ"
    },
    # RSA Level
    {
        "id": 4,
        "level": 4,
        "algorithm": "RSA",
        "title": "Két Sắt Bí Mật",
        "description": "Một két sắt cổ được bảo vệ bởi hệ thống mật mã RSA hiện đại. Đây là thử thách khó khăn.",
        "story": "Chiếc két sắt cổ kính này chứa đựng bí mật quan trọng. Hệ thống bảo mật RSA đòi hỏi sự thông minh và kiên nhẫn.",
        "ciphertext": "Q1JZUFRPIEtITyBCQVUgTkFZIE8gREFZIQ==",
        "correct_key": "CRYPTO",
        "plaintext": "CRYPTO KHO BAU NAY O DAY!",
        "hint_1": "Mật mã RSA sử dụng cặp khóa công khai và riêng tư.",
        "hint_2": "Từ khóa liên quan đến khoa học mật mã học.",
        "hint_3": "Thử từ khóa 'CRYPTO' - viết tắt của Cryptography.",
        "points": 300,
        "difficulty": "Khó"
    },
    # Vigenère Cipher Level (khác key)
    {
        "id": 5,
        "level": 5,
        "algorithm": "Vigenère",
        "title": "Mật Thư Hoàng Gia",
        "description": "Một lá thư bí mật từ hoàng gia cổ, được mã hóa bằng Vigenère với từ khóa hoàng gia.",
        "story": "Lá thư mang con dấu hoàng gia, chứa đựng bí mật về vị trí kho báu. Từ khóa có thể liên quan đến quyền lực.",
        "ciphertext": "OSGG VTJZ SOYF WQEJ GLJH VSMY WMJZ",
        "correct_key": "KING",
        "plaintext": "EVER GOLD COIN HERE MUST KEEP SAFE",
        "hint_1": "Từ khóa liên quan đến quyền lực và hoàng gia.",
        "hint_2": "Thử các từ như KING, QUEEN, ROYAL.",
        "hint_3": "Từ khóa là 'KING' - vua trong tiếng Anh.",
        "points": 250,
        "difficulty": "Trung bình"
    },
    # AES Level
    {
        "id": 6,
        "level": 6,
        "algorithm": "AES",
        "title": "Hầm Mộ Cổ Đại",
        "description": "Trong hầm mộ cổ đại, Smith tìm thấy bia đá với mật mã AES hiện đại - ai đó đã từng ở đây!",
        "story": "Bia đá cổ nhưng có khắc chữ hiện đại. Ai đó đã sử dụng công nghệ mã hóa tiên tiến để bảo vệ bí mật này.",
        "ciphertext": "VFJFQVNVUkUyMDI0ISBLSE8gQkFVIERBIFRJTSBUSEFZIQ==",
        "correct_key": "TREASURE2024!",
        "plaintext": "TREASURE2024! KHO BAU DA TIM THAY!",
        "hint_1": "Mật mã AES là tiêu chuẩn mã hóa hiện đại.",
        "hint_2": "Khóa có thể là tên kho báu kèm theo năm hiện tại.",
        "hint_3": "Thử 'TREASURE2024!' - tên kho báu với năm 2024.",
        "points": 400,
        "difficulty": "Khó"
    },
    # Caesar Cipher Level (shift khác nữa)
    {
        "id": 7,
        "level": 7,
        "algorithm": "Caesar",
        "title": "Bản Đồ Cướp Biển",
        "description": "Bản đồ kho báu của cướp biển cổ, sử dụng mật mã Caesar đơn giản nhưng hiệu quả.",
        "story": "Bản đồ cũ kỹ với vết nước muối, Smith nhận ra đây là di tích của cướp biển. Họ thường dùng mã đơn giản nhưng khó đoán.",
        "ciphertext": "CVENGRQ ZNCF FUBJ GUR JNL GB GERNFHER",
        "correct_key": "13",
        "plaintext": "PIRATES MAPS SHOW THE WAY TO TREASURE",
        "hint_1": "Cướp biển thường dùng số may mắn của họ.",
        "hint_2": "Thử số 13 - số xui xẻo nhưng cướp biển lại thích.",
        "hint_3": "Khóa là 13 - ROT13 nổi tiếng.",
        "points": 120,
        "difficulty": "Dễ"
    },
    # RSA Level (khác key)
    {
        "id": 8,
        "level": 8,
        "algorithm": "RSA",
        "title": "Kho Máy Tính Cổ",
        "description": "Trong phòng lab cũ, Smith tìm thấy máy tính cổ với thông điệp RSA còn hiển thị trên màn hình.",
        "story": "Màn hình máy tính cổ vẫn còn sáng sau nhiều năm. Thông điệp RSA này dường như đang chờ ai đó giải mã.",
        "ciphertext": "U0VDUkVUIENPREUgSEVSRSBJUyBTQUZFIQ==",
        "correct_key": "SECRET",
        "plaintext": "SECRET CODE HERE IS SAFE!",
        "hint_1": "Từ khóa liên quan đến bí mật và an toàn.",
        "hint_2": "Thử từ SECRET, PASSWORD, SECURE.",
        "hint_3": "Từ khóa là 'SECRET' - bí mật.",
        "points": 350,
        "difficulty": "Khó"
    },
    # AES Level cuối
    {
        "id": 9,
        "level": 9,
        "algorithm": "AES",
        "title": "Kho Báu Cuối Cùng",
        "description": "Thử thách cuối cùng! Kho báu thực sự được bảo vệ bởi mật mã AES mạnh nhất. Smith đã gần đến đích rồi!",
        "story": "Đây là nơi kho báu thực sự được giấu. Lớp bảo vệ cuối cùng này sử dụng AES với khóa phức tạp nhất.",
        "ciphertext": "RklOQUwgVFJFQVNVUkUgSU4gVEhJUyBQTEFDRSEgU01JVEggV0lOUyE=",
        "correct_key": "FINAL_TREASURE_2024",
        "plaintext": "FINAL TREASURE IN THIS PLACE! SMITH WINS!",
        "hint_1": "Đây là kho báu cuối cùng, khóa sẽ liên quan đến điều này.",
        "hint_2": "Khóa có thể là FINAL_TREASURE kèm năm.",
        "hint_3": "Thử 'FINAL_TREASURE_2024' - kho báu cuối cùng 2024.",
        "points": 500,
        "difficulty": "Rất khó"
    }
]

@app.route('/')
def index():
    return render_template('index.html', puzzles=PUZZLES)

@app.route('/api/levels')
def get_levels():
    return jsonify(PUZZLES)

@app.route('/api/attempt', methods=['POST'])
def check_attempt():
    data = request.get_json()
    level_id = data.get('level_id')
    attempted_key = data.get('attempted_key', '').strip()
    
    # Find the puzzle
    puzzle = None
    for p in PUZZLES:
        if p['id'] == level_id:
            puzzle = p
            break
    
    if not puzzle:
        return jsonify({'error': 'Level không tồn tại'}), 404
    
    # Check if the key is correct
    is_correct = False
    decrypted_text = ""
    
    try:
        if puzzle['algorithm'] == 'Caesar':
            is_correct, decrypted_text = CryptoUtils.check_caesar(
                puzzle['ciphertext'], 
                attempted_key, 
                puzzle['correct_key']
            )
        elif puzzle['algorithm'] == 'Vigenère':
            is_correct, decrypted_text = CryptoUtils.check_vigenere(
                puzzle['ciphertext'], 
                attempted_key, 
                puzzle['correct_key']
            )
        elif puzzle['algorithm'] == 'RSA':
            is_correct, decrypted_text = CryptoUtils.check_rsa(
                puzzle['ciphertext'], 
                attempted_key, 
                puzzle['correct_key']
            )
        elif puzzle['algorithm'] == 'AES':
            is_correct, decrypted_text = CryptoUtils.check_aes(
                puzzle['ciphertext'], 
                attempted_key, 
                puzzle['correct_key']
            )
    except Exception as e:
        return jsonify({'error': f'Lỗi giải mã: {str(e)}'}), 400
    
    if is_correct:
        points_earned = puzzle['points']
        return jsonify({
            'correct': True,
            'plaintext': decrypted_text or puzzle['plaintext'],
            'points_earned': points_earned,
            'message': f'Xuất sắc! Bạn đã giải mã thành công level {level_id}!'
        })
    else:
        return jsonify({
            'correct': False,
            'message': 'Khóa không đúng. Hãy thử lại!'
        })

@app.route('/api/player/create', methods=['POST'])
def create_player():
    data = request.get_json()
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    
    if not username:
        return jsonify({'error': 'Tên thám tử không được để trống'}), 400
    
    # In a real app, you'd save this to a database
    player_data = {
        'username': username,
        'email': email,
        'current_level': 1,
        'total_score': 0,
        'completed_levels': []
    }
    
    return jsonify({
        'success': True,
        'player': player_data,
        'message': f'Chào mừng thám tử {username}!'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
