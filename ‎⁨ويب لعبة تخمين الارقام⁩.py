<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لعبة الذاكرة 🧠</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .game-container {
            background: white;
            border-radius: 30px;
            padding: 30px;
            max-width: 500px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }

        .header {
            text-align: center;
            margin-bottom: 20px;
        }

        .header h1 {
            color: #667eea;
            font-size: 32px;
            margin-bottom: 5px;
        }

        .header .subtitle {
            color: #888;
            font-size: 14px;
        }

        .stats {
            display: flex;
            justify-content: space-between;
            margin-bottom: 15px;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 15px;
        }

        .stat-item {
            text-align: center;
            flex: 1;
        }

        .stat-item .label {
            font-size: 12px;
            color: #888;
        }

        .stat-item .value {
            font-size: 20px;
            font-weight: bold;
            color: #333;
        }

        .stat-item .value.time {
            color: #ff6b6b;
        }

        .stat-item .value.attempts {
            color: #feca57;
        }

        .stat-item .value.best {
            color: #667eea;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            margin: 20px 0;
        }

        .card {
            aspect-ratio: 1;
            background: #e0e0e0;
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 32px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 3px solid #ccc;
            color: #333;
            user-select: none;
        }

        .card:hover:not(.matched):not(.disabled) {
            transform: scale(1.05);
            border-color: #667eea;
        }

        .card.revealed {
            background: #ffd93d;
            border-color: #f6b93b;
        }

        .card.matched {
            background: #6bcf7f;
            border-color: #27ae60;
            cursor: default;
            transform: scale(0.95);
        }

        .card.wrong {
            background: #ff6b6b;
            border-color: #c0392b;
        }

        .card.hidden {
            background: #e0e0e0;
            color: transparent;
        }

        .card.disabled {
            cursor: not-allowed;
            opacity: 0.7;
        }

        .controls {
            display: flex;
            gap: 10px;
            margin-top: 20px;
        }

        .btn {
            flex: 1;
            padding: 15px;
            border: none;
            border-radius: 15px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            color: white;
        }

        .btn-primary {
            background: #667eea;
        }

        .btn-primary:hover {
            background: #5a67d8;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        .btn-success {
            background: #6bcf7f;
        }

        .btn-success:hover {
            background: #5cb85c;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(107, 207, 127, 0.4);
        }

        .btn-warning {
            background: #feca57;
            color: #333;
        }

        .btn-warning:hover {
            background: #fdcb6e;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(254, 202, 87, 0.4);
        }

        .message {
            text-align: center;
            margin-top: 15px;
            padding: 15px;
            border-radius: 15px;
            font-weight: bold;
            display: none;
        }

        .message.show {
            display: block;
        }

        .message.success {
            background: #d4edda;
            color: #155724;
            border: 2px solid #b8daff;
        }

        .message.info {
            background: #d1ecf1;
            color: #0c5460;
            border: 2px solid #bee5eb;
        }

        @media (max-width: 400px) {
            .game-container {
                padding: 15px;
            }
            
            .card {
                font-size: 24px;
            }
            
            .header h1 {
                font-size: 24px;
            }
            
            .stats {
                flex-wrap: wrap;
            }
            
            .stat-item {
                min-width: 45%;
            }
        }
    </style>
</head>
<body>
    <div class="game-container">
        <div class="header">
            <h1>🧠 لعبة الذاكرة</h1>
            <div class="subtitle">تذكر الأزواج المتطابقة</div>
        </div>

        <div class="stats">
            <div class="stat-item">
                <div class="label">⏱️ الوقت</div>
                <div class="value time" id="timer">0</div>
            </div>
            <div class="stat-item">
                <div class="label">🎯 المحاولات</div>
                <div class="value attempts" id="attempts">0</div>
            </div>
            <div class="stat-item">
                <div class="label">🏆 أفضل محاولات</div>
                <div class="value best" id="bestScore">-</div>
            </div>
        </div>

        <div class="grid" id="grid"></div>

        <div class="controls">
            <button class="btn btn-primary" onclick="restartGame()">🔄 إعادة التشغيل</button>
            <button class="btn btn-success" onclick="showBest()">🏆 أفضل نتيجة</button>
        </div>

        <div class="message" id="message"></div>
    </div>

    <script>
        // متغيرات اللعبة
        let cards = [];
        let cardValues = [];
        let matchedPairs = 0;
        let firstCard = null;
        let secondCard = null;
        let lockBoard = false;
        let attempts = 0;
        let bestScore = localStorage.getItem('memoryBestScore');
        let bestTime = localStorage.getItem('memoryBestTime');
        let timer = 0;
        let timerInterval = null;
        let gameStarted = false;

        const grid = document.getElementById('grid');
        const timerDisplay = document.getElementById('timer');
        const attemptsDisplay = document.getElementById('attempts');
        const bestScoreDisplay = document.getElementById('bestScore');
        const messageDisplay = document.getElementById('message');

        // تحديث عرض أفضل نتيجة
        function updateBestDisplay() {
            if (bestScore) {
                bestScoreDisplay.textContent = bestScore;
            } else {
                bestScoreDisplay.textContent = '-';
            }
        }

        // إنشاء الأرقام
        function generateNumbers() {
            const numbers = [];
            for (let i = 1; i <= 8; i++) {
                numbers.push(i, i);
            }
            return shuffleArray(numbers);
        }

        // خلط المصفوفة
        function shuffleArray(array) {
            for (let i = array.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [array[i], array[j]] = [array[j], array[i]];
            }
            return array;
        }

        // إنشاء البطاقات
        function createCards() {
            const values = generateNumbers();
            cardValues = values;
            grid.innerHTML = '';
            cards = [];

            values.forEach((value, index) => {
                const card = document.createElement('div');
                card.className = 'card hidden';
                card.dataset.index = index;
                card.dataset.value = value;
                card.textContent = value;
                card.addEventListener('click', () => flipCard(card));
                grid.appendChild(card);
                cards.push(card);
            });
        }

        // قلب البطاقة
        function flipCard(card) {
            if (lockBoard) return;
            if (card === firstCard) return;
            if (card.classList.contains('matched')) return;
            if (card.classList.contains('revealed')) return;

            // بدء المؤقت عند أول نقرة
            if (!gameStarted) {
                startTimer();
                gameStarted = true;
            }

            card.classList.remove('hidden');
            card.classList.add('revealed');

            if (!firstCard) {
                firstCard = card;
                return;
            }

            secondCard = card;
            attempts++;
            attemptsDisplay.textContent = attempts;
            lockBoard = true;

            checkMatch();
        }

        // التحقق من التطابق
        function checkMatch() {
            const value1 = firstCard.dataset.value;
            const value2 = secondCard.dataset.value;

            if (value1 === value2) {
                // تطابق
                firstCard.classList.remove('revealed');
                secondCard.classList.remove('revealed');
                firstCard.classList.add('matched');
                secondCard.classList.add('matched');
                matchedPairs++;

                if (matchedPairs === 8) {
                    // فوز
                    stopTimer();
                    const timeStr = formatTime(timer);
                    const evaluation = evaluatePerformance(attempts);
                    
                    // تحديث أفضل نتيجة
                    let isNewRecord = false;
                    if (!bestScore || attempts < parseInt(bestScore)) {
                        bestScore = attempts;
                        bestTime = timer;
                        localStorage.setItem('memoryBestScore', bestScore);
                        localStorage.setItem('memoryBestTime', bestTime);
                        isNewRecord = true;
                        updateBestDisplay();
                    } else if (attempts === parseInt(bestScore) && (!bestTime || timer < parseFloat(bestTime))) {
                        bestTime = timer;
                        localStorage.setItem('memoryBestTime', bestTime);
                        isNewRecord = true;
                    }

                    const bestScoreText = bestScore ? `${bestScore} محاولات` : 'لا يوجد';
                    const bestTimeText = bestTime ? formatTime(bestTime) : 'لا يوجد';
                    
                    let message = `🎉 مبروك! أنت فزت!\nالمحاولات: ${attempts}\nالوقت: ${timeStr}\n${evaluation}`;
                    if (isNewRecord) {
                        message = `🏆 رقم قياسي جديد! 🏆\n${message}\n\nأفضل محاولات: ${bestScoreText}\nأفضل وقت: ${bestTimeText}`;
                    } else {
                        message = `${message}\n\n🏆 أفضل محاولات: ${bestScoreText}\n🏆 أفضل وقت: ${bestTimeText}`;
                    }
                    
                    showMessage(message, 'success');
                    lockBoard = true;
                }

                resetTurn();
            } else {
                // غير متطابق
                firstCard.classList.add('wrong');
                secondCard.classList.add('wrong');

                setTimeout(() => {
                    firstCard.classList.remove('revealed', 'wrong');
                    secondCard.classList.remove('revealed', 'wrong');
                    firstCard.classList.add('hidden');
                    secondCard.classList.add('hidden');
                    resetTurn();
                }, 800);
            }
        }

        // إعادة تعيين الدور
        function resetTurn() {
            firstCard = null;
            secondCard = null;
            lockBoard = false;
        }

        // بدء المؤقت
        function startTimer() {
            if (timerInterval) return;
            timer = 0;
            timerInterval = setInterval(() => {
                timer++;
                timerDisplay.textContent = timer;
            }, 1000);
        }

        // إيقاف المؤقت
        function stopTimer() {
            if (timerInterval) {
                clearInterval(timerInterval);
                timerInterval = null;
            }
        }

        // إعادة تعيين المؤقت
        function resetTimer() {
            stopTimer();
            timer = 0;
            timerDisplay.textContent = '0';
            gameStarted = false;
        }

        // تنسيق الوقت
        function formatTime(seconds) {
            const mins = Math.floor(seconds / 60);
            const secs = seconds % 60;
            if (mins > 0) {
                return `${mins}:${secs.toString().padStart(2, '0')}`;
            }
            return `${secs} ثانية`;
        }

        // تقييم الأداء
        function evaluatePerformance(attempts) {
            if (attempts <= 8) return '🏆 أسطورة الذاكرة! أداء خارق!';
            if (attempts <= 10) return '⭐ ممتاز! ذاكرة قوية جداً!';
            if (attempts <= 13) return '👍 جيد جداً! ذاكرة جيدة!';
            if (attempts <= 16) return '😐 متوسط، تحتاج إلى تمرين أكثر!';
            if (attempts <= 20) return '😅 يحتاج تدريب، حاول مرة أخرى!';
            return '🤯 لا بأس، الممارسة تجعلها أفضل!';
        }

        // عرض رسالة
        function showMessage(text, type = 'info') {
            messageDisplay.textContent = text;
            messageDisplay.className = `message show ${type}`;
        }

        // إخفاء الرسالة
        function hideMessage() {
            messageDisplay.className = 'message';
        }

        // إعادة تشغيل اللعبة
        function restartGame() {
            hideMessage();
            resetTimer();
            attempts = 0;
            matchedPairs = 0;
            attemptsDisplay.textContent = '0';
            lockBoard = false;
            firstCard = null;
            secondCard = null;
            createCards();
            // عرض البطاقات لمدة 3 ثواني
            showAllCards();
            setTimeout(() => {
                hideAllCards();
            }, 3000);
        }

        // عرض جميع البطاقات
        function showAllCards() {
            cards.forEach(card => {
                card.classList.remove('hidden');
                card.classList.add('revealed');
            });
        }

        // إخفاء جميع البطاقات
        function hideAllCards() {
            cards.forEach(card => {
                if (!card.classList.contains('matched')) {
                    card.classList.remove('revealed');
                    card.classList.add('hidden');
                }
            });
            lockBoard = false;
        }

        // عرض أفضل نتيجة
        function showBest() {
            if (bestScore) {
                const timeText = bestTime ? formatTime(bestTime) : 'غير مسجل';
                showMessage(`🏆 أفضل محاولات: ${bestScore}\n⏱️ أفضل وقت: ${timeText}`, 'info');
            } else {
                showMessage('لا توجد نتائج مسجلة بعد. العب وسجل رقمك القياسي! 🎯', 'info');
            }
        }

        // بدء اللعبة
        function initGame() {
            updateBestDisplay();
            createCards();
            // عرض البطاقات لمدة 3 ثواني
            showAllCards();
            setTimeout(() => {
                hideAllCards();
            }, 3000);
        }

        // بدء التشغيل
        initGame();
    </script>
</body>
</html>
