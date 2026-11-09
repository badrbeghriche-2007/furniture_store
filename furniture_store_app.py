# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, redirect
import urllib.parse

app = Flask(__name__)

# رقم الواتساب بصيغة الجزائر الدولية (213)
WHATSAPP_NUMBER = "213784803429"

# كود واجهة المستخدم HTML + Tailwind CSS + JavaScript
HTML_PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>دار الأناقة | بيع الأثاث والمرايا</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Tajawal', sans-serif; background-color: #FCFBF9; }
        .product-card { transition: all 0.35s ease; }
        .product-card:hover { transform: translateY(-8px); box-shadow: 0 20px 35px -10px rgba(100, 75, 50, 0.15); }
    </style>
</head>
<body class="min-h-screen text-[#3D3124] flex flex-col justify-between">

    <!-- الهيدر -->
    <header class="bg-white/90 border-b border-[#ECE4D5] sticky top-0 z-30 shadow-sm">
        <div class="max-w-6xl mx-auto px-4 h-20 flex items-center justify-between">
            <h1 class="text-2xl font-extrabold text-[#53412C]">دار الأناقة</h1>
            <span class="text-sm font-semibold text-[#7D623F]">واتساب: <b dir="ltr">0784803429</b></span>
        </div>
    </header>

    <!-- المنتجات -->
    <main class="max-w-5xl mx-auto px-4 py-12 flex-grow w-full">
        <div class="text-center mb-12">
            <h2 class="text-3xl sm:text-4xl font-extrabold text-[#53412C] mb-3">أثاث عصري ومرايا ديكور راقية</h2>
            <p class="text-[#7D623F]">اختر المنتج الذي تريده لتعبئة معلومات التوصيل وإرسال الطلب فوراً عبر واتساب</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <!-- كارت الأثاث -->
            <div onclick="openOrderModal('أثاث صالون عصري فاخر', '65000 دج')" class="product-card cursor-pointer bg-white rounded-3xl border border-[#ECE4D5] p-7 flex flex-col justify-between">
                <div>
                    <div class="flex justify-between items-center mb-4">
                        <span class="text-xs font-bold bg-[#F6F2EB] text-[#7D623F] px-3 py-1 rounded-lg">الأثاث</span>
                        <span class="text-2xl font-black text-[#665035]">65,000 دج</span>
                    </div>
                    <h3 class="text-2xl font-bold mb-3 text-[#53412C]">أثاث صالون عصري فاخر</h3>
                    <p class="text-sm text-[#7D623F] leading-relaxed mb-6">طقم متكامل بتصميم ناعم ومريح باللونين الأبيض والبيج، مناسب لكافة المساحات العصرية.</p>
                </div>
                <button type="button" class="w-full bg-[#665035] hover:bg-[#53412C] text-white font-bold py-3.5 rounded-2xl transition">انقر للطلب (65000 دج)</button>
            </div>

            <!-- كارت المرآة -->
            <div onclick="openOrderModal('مرآة ديكور مقوسة فاخرة', '3000 دج')" class="product-card cursor-pointer bg-white rounded-3xl border border-[#ECE4D5] p-7 flex flex-col justify-between">
                <div>
                    <div class="flex justify-between items-center mb-4">
                        <span class="text-xs font-bold bg-[#F6F2EB] text-[#7D623F] px-3 py-1 rounded-lg">الديكور</span>
                        <span class="text-2xl font-black text-[#665035]">3,000 دج</span>
                    </div>
                    <h3 class="text-2xl font-bold mb-3 text-[#53412C]">مرآة ديكور مقوسة فاخرة</h3>
                    <p class="text-sm text-[#7D623F] leading-relaxed mb-6">مرآة مقوسة بنقاء عالي وإطار بلون البيج الذهبي، تضفي اتساعاً وإضاءة راقية لمنزلك.</p>
                </div>
                <button type="button" class="w-full bg-[#665035] hover:bg-[#53412C] text-white font-bold py-3.5 rounded-2xl transition">انقر للطلب (3000 دج)</button>
            </div>
        </div>
    </main>

    <!-- نافذة تعبئة معلومات الزبون (Popup Modal) -->
    <div id="orderModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm hidden items-center justify-center p-4 z-50">
        <div class="bg-white rounded-3xl border border-[#ECE4D5] max-w-lg w-full p-6 shadow-2xl relative">
            <div class="flex justify-between items-center mb-5 pb-3 border-b border-[#ECE4D5]">
                <div>
                    <h4 id="modalTitle" class="text-xl font-bold text-[#53412C]">طلب المنتج</h4>
                    <span id="modalPrice" class="text-sm font-extrabold text-[#7D623F]"></span>
                </div>
                <button type="button" onclick="closeOrderModal()" class="w-8 h-8 rounded-full bg-[#F6F2EB] text-sm font-bold">✕</button>
            </div>

            <form action="/submit_order" method="POST" target="_blank" class="space-y-3.5">
                <input type="hidden" name="product_name" id="hiddenProdName">
                <input type="hidden" name="product_price" id="hiddenProdPrice">

                <div class="grid grid-cols-2 gap-3">
                    <div>
                        <label class="block text-xs font-bold mb-1">الاسم *</label>
                        <input type="text" name="first_name" required placeholder="الاسم" class="w-full px-3.5 py-2.5 rounded-xl bg-[#FCFBF9] border border-[#ECE4D5] text-sm focus:outline-none focus:border-[#7D623F]">
                    </div>
                    <div>
                        <label class="block text-xs font-bold mb-1">اللقب *</label>
                        <input type="text" name="last_name" required placeholder="اللقب" class="w-full px-3.5 py-2.5 rounded-xl bg-[#FCFBF9] border border-[#ECE4D5] text-sm focus:outline-none focus:border-[#7D623F]">
                    </div>
                </div>

                <div>
                    <label class="block text-xs font-bold mb-1">رقم الهاتف *</label>
                    <input type="tel" name="phone" required placeholder="07 / 06 / 05 XX XX XX XX" class="w-full px-3.5 py-2.5 rounded-xl bg-[#FCFBF9] border border-[#ECE4D5] text-sm focus:outline-none focus:border-[#7D623F]">
                </div>

                <div>
                    <label class="block text-xs font-bold mb-1">البريد الإلكتروني *</label>
                    <input type="email" name="email" required placeholder="name@example.com" class="w-full px-3.5 py-2.5 rounded-xl bg-[#FCFBF9] border border-[#ECE4D5] text-sm focus:outline-none focus:border-[#7D623F]">
                </div>

                <div>
                    <label class="block text-xs font-bold mb-1">مكان السكن (العنوان والولاية) *</label>
                    <input type="text" name="address" required placeholder="الولاية، الدائرة أو البلدية، العنوان" class="w-full px-3.5 py-2.5 rounded-xl bg-[#FCFBF9] border border-[#ECE4D5] text-sm focus:outline-none focus:border-[#7D623F]">
                </div>

                <button type="submit" class="w-full mt-3 bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-3.5 rounded-2xl shadow-lg transition">
                    طلب وإرسال عبر واتساب (0784803429)
                </button>
            </form>
        </div>
    </div>

    <script>
        function openOrderModal(name, price) {
            document.getElementById('modalTitle').textContent = name;
            document.getElementById('modalPrice').textContent = "السعر: " + price;
            document.getElementById('hiddenProdName').value = name;
            document.getElementById('hiddenProdPrice').value = price;
            const modal = document.getElementById('orderModal');
            modal.classList.remove('hidden');
            modal.classList.add('flex');
        }
        function closeOrderModal() {
            const modal = document.getElementById('orderModal');
            modal.classList.add('hidden');
            modal.classList.remove('flex');
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@app.route("/submit_order", methods=["POST"])
def submit_order():
    first_name = request.form.get("first_name", "").strip()
    last_name = request.form.get("last_name", "").strip()
    full_name = f"{first_name} {last_name}".strip()
    
    phone = request.form.get("phone", "").strip()
    email = request.form.get("email", "").strip()
    address = request.form.get("address", "").strip()
    product_name = request.form.get("product_name", "منتج")
    product_price = request.form.get("product_price", "")

    # صياغة رسالة الواتساب باسم صاحب الطلب
    message = (
        f"🛒 *طلب جديد باسم: {full_name}*\\n"
        f"━━━━━━━━━━━━━━━\\n"
        f"📦 *المنتج:* {product_name}\\n"
        f"💰 *السعر:* {product_price}\\n"
        f"━━━━━━━━━━━━━━━\\n"
        f"👤 *الاسم:* {first_name}\\n"
        f"👤 *اللقب:* {last_name}\\n"
        f"📞 *الهاتف:* {phone}\\n"
        f"📧 *البريد:* {email}\\n"
        f"📍 *مكان السكن:* {address}\\n"
        f"━━━━━━━━━━━━━━━\\n"
        f"مرسل من طرف الزبون: *{full_name}*"
    )
    
    encoded_message = urllib.parse.quote(message)
    whatsapp_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_message}"
    return redirect(whatsapp_url)

if __name__ == "__main__":
    app.run(debug=True, port=5000)