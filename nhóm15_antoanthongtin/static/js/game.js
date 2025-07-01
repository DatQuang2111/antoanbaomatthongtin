/**
 * Cryptography Treasure Hunt Game
 * Vietnamese Language Support
 */

class CryptographyGame {
    constructor() {
        this.currentPlayer = null;
        this.levels = [];
        this.currentLevel = null;
        this.currentLevelId = 1;
        this.gameStartTime = null;
        this.hintsUsed = 0;
        this.totalScore = 0;
        
        this.init();
    }

    async init() {
        this.showLoadingScreen();
        this.setupEventListeners();
        await this.loadLevels();
        this.setupNavigation();
        
        setTimeout(() => {
            this.hideLoadingScreen();
            this.showSection('home');
        }, 2000);
    }

    showLoadingScreen() {
        const loadingScreen = document.getElementById('loadingScreen');
        const progressBar = document.getElementById('loadingProgress');
        let progress = 0;
        
        const interval = setInterval(() => {
            progress += Math.random() * 15 + 5;
            if (progress >= 100) {
                progress = 100;
                clearInterval(interval);
            }
            progressBar.style.width = progress + '%';
        }, 150);
    }

    hideLoadingScreen() {
        const loadingScreen = document.getElementById('loadingScreen');
        loadingScreen.style.opacity = '0';
        setTimeout(() => {
            loadingScreen.style.display = 'none';
        }, 500);
    }

    setupEventListeners() {
        // Registration form
        const registrationForm = document.getElementById('registrationForm');
        if (registrationForm) {
            registrationForm.addEventListener('submit', (e) => this.handleRegistration(e));
        }

        // Challenge input
        const submitBtn = document.getElementById('submitAnswer');
        const keyInput = document.getElementById('decryptionKey');
        
        if (submitBtn) {
            submitBtn.addEventListener('click', () => this.submitAnswer());
        }
        
        if (keyInput) {
            keyInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.submitAnswer();
                }
            });
        }

        // Hint button
        const hintBtn = document.getElementById('hintBtn');
        if (hintBtn) {
            hintBtn.addEventListener('click', () => this.showHint());
        }

        // Modal close buttons
        document.querySelectorAll('.modal-close').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.target.closest('.modal').classList.remove('show');
            });
        });

        // Next level button
        const nextLevelBtn = document.getElementById('nextLevelBtn');
        if (nextLevelBtn) {
            nextLevelBtn.addEventListener('click', () => this.goToNextLevel());
        }

        // Click outside modal to close
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    modal.classList.remove('show');
                }
            });
        });
    }

    setupNavigation() {
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const targetSection = link.getAttribute('href').substring(1);
                this.showSection(targetSection);
                
                // Update active nav link
                document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
                link.classList.add('active');
            });
        });
    }

    showSection(sectionId) {
        document.querySelectorAll('.section').forEach(section => {
            section.classList.remove('active');
        });
        
        const targetSection = document.getElementById(sectionId);
        if (targetSection) {
            targetSection.classList.add('active');
        }
    }

    async loadLevels() {
        try {
            console.log('Loading levels from API...');
            const response = await fetch('/api/levels');
            console.log('API response status:', response.status);
            this.levels = await response.json();
            console.log('Loaded levels:', this.levels.length);
            this.renderLevels();
        } catch (error) {
            console.error('Error loading levels:', error);
            this.showToast('Lỗi tải dữ liệu game', 'error');
        }
    }

    renderLevels() {
        const levelsGrid = document.getElementById('levelsGrid');
        if (!levelsGrid) {
            console.error('levelsGrid element not found!');
            return;
        }

        console.log('Rendering', this.levels.length, 'levels');
        levelsGrid.innerHTML = '';

        this.levels.forEach(level => {
            const levelCard = this.createLevelCard(level);
            levelsGrid.appendChild(levelCard);
        });
        
        console.log('Levels rendered successfully');
    }

    createLevelCard(level) {
        const isCompleted = this.currentPlayer && level.id < this.currentLevelId;
        const isCurrent = level.id === this.currentLevelId;
        // Cho phép chơi level hiện tại và các level trước đó nếu đã đăng ký
        const isLocked = !this.currentPlayer || level.id > this.currentLevelId;

        const card = document.createElement('div');
        card.className = `level-card ${isCompleted ? 'completed' : ''} ${isCurrent ? 'current' : ''} ${isLocked ? 'locked' : ''}`;
        
        card.innerHTML = `
            <div class="level-header">
                <div class="level-number">${level.id}</div>
                <div class="difficulty ${level.difficulty.toLowerCase().replace(' ', '-')}">${level.difficulty}</div>
            </div>
            <h3 class="level-title">${level.title}</h3>
            <p class="level-description">${level.description}</p>
            <div class="level-meta">
                <span class="algorithm">${level.algorithm}</span>
                <span class="level-points">+${level.points} điểm</span>
            </div>
            ${isCompleted ? '<div class="completion-badge"><i class="fas fa-check-circle"></i></div>' : ''}
            ${isLocked ? '<div class="lock-badge"><i class="fas fa-lock"></i></div>' : ''}
        `;

        // Cho phép click vào level hiện tại hoặc đã hoàn thành
        if (!isLocked || isCompleted || isCurrent) {
            card.addEventListener('click', () => this.selectLevel(level));
        }

        return card;
    }

    selectLevel(level) {
        if (!this.currentPlayer) {
            this.showToast('Vui lòng đăng ký trước khi chơi', 'warning');
            this.showSection('home');
            return;
        }

        // Check if level is accessible
        if (level.id > this.currentLevelId) {
            this.showToast('Hãy hoàn thành level trước đó trước!', 'warning');
            return;
        }

        console.log('Selecting level:', level.id, level.title);
        this.currentLevel = level;
        this.hintsUsed = 0;
        this.gameStartTime = Date.now();
        
        this.updateChallengeDisplay();
        this.updateHintButton();
        
        // Show challenge section
        const challengeSection = document.getElementById('currentChallenge');
        if (challengeSection) {
            challengeSection.style.display = 'block';
            challengeSection.scrollIntoView({ 
                behavior: 'smooth' 
            });
        }
        
        // Debug input field
        setTimeout(() => {
            const keyInput = document.getElementById('decryptionKey');
            if (keyInput) {
                console.log('Input field properties:');
                console.log('- disabled:', keyInput.disabled);
                console.log('- readOnly:', keyInput.readOnly);
                console.log('- value:', keyInput.value);
                console.log('- style.display:', keyInput.style.display);
                console.log('- offsetWidth:', keyInput.offsetWidth);
                console.log('- offsetHeight:', keyInput.offsetHeight);
            } else {
                console.error('Input field not found!');
            }
        }, 500);
    }

    updateChallengeDisplay() {
        if (!this.currentLevel) return;

        document.getElementById('challengeTitle').textContent = this.currentLevel.title;
        document.getElementById('challengeDifficulty').textContent = this.currentLevel.difficulty;
        document.getElementById('challengeAlgorithm').textContent = this.currentLevel.algorithm;
        document.getElementById('challengeStory').textContent = this.currentLevel.story;
        
        // Show cipher
        const cipherDisplay = document.getElementById('cipherDisplay');
        const cipherText = document.getElementById('cipherText');
        if (cipherDisplay && cipherText) {
            cipherDisplay.style.display = 'block';
            cipherText.textContent = this.currentLevel.ciphertext;
        }
        
        // Show input
        const challengeInput = document.getElementById('challengeInput');
        if (challengeInput) {
            challengeInput.style.display = 'block';
        }
        
        // Clear previous input and enable it
        const keyInput = document.getElementById('decryptionKey');
        const submitBtn = document.getElementById('submitAnswer');
        if (keyInput) {
            keyInput.value = '';
            keyInput.disabled = false;
            keyInput.readOnly = false;
            keyInput.style.pointerEvents = 'auto';
            keyInput.style.cursor = 'text';
            console.log('Input field enabled and focused');
            setTimeout(() => keyInput.focus(), 100);
        }
        if (submitBtn) {
            submitBtn.disabled = false;
        }
        
        // Reset hint button
        const hintBtn = document.getElementById('hintBtn');
        if (hintBtn) {
            hintBtn.disabled = false;
            hintBtn.innerHTML = '<i class="fas fa-lightbulb"></i> Gợi Ý (<span id="hintsUsed">0</span>/3)';
        }
    }

    async submitAnswer() {
        if (!this.currentLevel || !this.currentPlayer) return;

        const keyInput = document.getElementById('decryptionKey');
        const attemptedKey = keyInput.value.trim();
        
        if (!attemptedKey) {
            this.showToast('Vui lòng nhập khóa giải mã', 'warning');
            return;
        }

        const timeSpent = Math.floor((Date.now() - this.gameStartTime) / 1000);
        
        try {
            const response = await fetch('/api/attempt', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    level_id: this.currentLevel.id,
                    attempted_key: attemptedKey,
                    time_spent: timeSpent,
                    hints_used: this.hintsUsed
                })
            });

            const result = await response.json();
            
            if (result.correct) {
                this.handleCorrectAnswer(result);
            } else {
                this.handleIncorrectAnswer();
            }
        } catch (error) {
            console.error('Error submitting answer:', error);
            this.showToast('Lỗi kết nối với server', 'error');
        }
    }

    handleCorrectAnswer(result) {
        // Update total score
        this.totalScore += result.points_earned;
        this.updatePlayerStats();
        
        // Show success modal
        document.getElementById('successMessage').textContent = 
            `Xuất sắc! Bạn đã giải mã thành công cấp độ ${this.currentLevel.id}!`;
        document.getElementById('successPlaintext').textContent = result.plaintext;
        document.getElementById('successPoints').textContent = `+${result.points_earned} điểm`;
        
        document.getElementById('successModal').classList.add('show');
        
        // Update current level - chỉ tăng nếu đây là level hiện tại
        if (this.currentLevel.id === this.currentLevelId) {
            this.currentLevelId = Math.min(this.currentLevelId + 1, this.levels.length + 1);
        }
        
        // Re-render levels
        this.renderLevels();
        
        this.showToast('Chúc mừng! Bạn đã hoàn thành thử thách!', 'success');
        
        // Check if game completed
        if (this.currentLevelId > this.levels.length) {
            setTimeout(() => {
                this.showGameComplete();
            }, 2000);
        }
    }

    handleIncorrectAnswer() {
        this.showToast('Khóa không đúng. Hãy thử lại!', 'error');
        
        // Clear input and focus
        const keyInput = document.getElementById('decryptionKey');
        keyInput.value = '';
        keyInput.focus();
        
        // Add shake animation
        keyInput.classList.add('shake');
        setTimeout(() => {
            keyInput.classList.remove('shake');
        }, 500);
    }

    goToNextLevel() {
        // Close modal
        document.getElementById('successModal').classList.remove('show');
        
        // Find next level
        const nextLevel = this.levels.find(l => l.id === this.currentLevelId);
        if (nextLevel) {
            this.selectLevel(nextLevel);
        } else {
            // Game completed
            this.showGameComplete();
        }
    }

    showHint() {
        if (!this.currentLevel) return;
        
        if (this.hintsUsed >= 3) {
            this.showToast('Bạn đã sử dụng hết gợi ý cho level này', 'warning');
            return;
        }
        
        let hintText = '';
        switch (this.hintsUsed) {
            case 0:
                hintText = this.currentLevel.hint_1;
                break;
            case 1:
                hintText = this.currentLevel.hint_2;
                break;
            case 2:
                hintText = this.currentLevel.hint_3;
                break;
        }
        
        document.getElementById('hintText').textContent = hintText;
        document.getElementById('hintModal').classList.add('show');
        
        this.hintsUsed++;
        this.updateHintButton();
    }

    updateHintButton() {
        const hintsUsedSpan = document.getElementById('hintsUsed');
        if (hintsUsedSpan) {
            hintsUsedSpan.textContent = this.hintsUsed;
        }
        
        const hintBtn = document.getElementById('hintBtn');
        if (hintBtn && this.hintsUsed >= 3) {
            hintBtn.disabled = true;
            hintBtn.innerHTML = '<i class="fas fa-lightbulb"></i> Hết gợi ý';
        }
    }

    async handleRegistration(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const username = formData.get('username').trim();
        const email = formData.get('email').trim();
        
        if (!username) {
            this.showToast('Vui lòng nhập tên thám tử', 'warning');
            return;
        }
        
        try {
            const response = await fetch('/api/player/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, email })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.currentPlayer = result.player;
                this.showToast(result.message, 'success');
                
                // Update UI
                this.updatePlayerStats();
                this.renderLevels();
                
                // Switch to game section
                setTimeout(() => {
                    this.showSection('game');
                    document.querySelector('.nav-link[href="#game"]').click();
                }, 1000);
            } else {
                this.showToast(result.error || 'Lỗi đăng ký', 'error');
            }
        } catch (error) {
            console.error('Error creating player:', error);
            this.showToast('Lỗi kết nối với server', 'error');
        }
    }

    updatePlayerStats() {
        if (!this.currentPlayer) return;
        
        const playerStats = document.getElementById('playerStats');
        const playerName = document.getElementById('currentPlayerName');
        const playerScore = document.getElementById('currentPlayerScore');
        const playerLevel = document.getElementById('currentPlayerLevel');
        
        if (playerStats) {
            playerStats.style.display = 'flex';
        }
        
        if (playerName) {
            playerName.textContent = this.currentPlayer.username;
        }
        
        if (playerScore) {
            playerScore.textContent = this.totalScore.toLocaleString();
        }
        
        if (playerLevel) {
            playerLevel.textContent = this.currentLevelId;
        }
    }

    showGameComplete() {
        document.getElementById('finalTotalScore').textContent = this.totalScore.toLocaleString();
        document.getElementById('gameCompleteModal').classList.add('show');
        
        // Hide challenge section
        document.getElementById('currentChallenge').style.display = 'none';
        
        this.showToast('🎉 Chúc mừng! Bạn đã hoàn thành game!', 'success');
    }

    showToast(message, type = 'info') {
        const toastContainer = document.getElementById('toastContainer');
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        
        toastContainer.appendChild(toast);
        
        // Show animation
        setTimeout(() => {
            toast.classList.add('show');
        }, 100);
        
        // Hide after 4 seconds
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
            }, 300);
        }, 4000);
    }
}

// Initialize game when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.game = new CryptographyGame();
});
