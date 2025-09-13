class FinanceRAGApp {
    constructor() {
        this.isInitialized = false;
        this.isLoading = false;
        this.chatMessages = [];
        
        this.initializeElements();
        this.bindEvents();
        this.loadSampleQuestions();
        this.checkStatus();
    }
    
    initializeElements() {
        // DOM elementleri
        this.elements = {
            // Buttons
            initializeBtn: document.getElementById('initializeBtn'),
            sendBtn: document.getElementById('sendBtn'),
            closeErrorModal: document.getElementById('closeErrorModal'),
            closeErrorBtn: document.getElementById('closeErrorBtn'),
            
            // Sections
            welcomeSection: document.getElementById('welcomeSection'),
            chatSection: document.getElementById('chatSection'),
            
            // Status
            statusIndicator: document.getElementById('statusIndicator'),
            statusDot: document.querySelector('.status-dot'),
            statusText: document.querySelector('.status-text'),
            
            // Chat
            questionInput: document.getElementById('questionInput'),
            chatMessages: document.getElementById('chatMessages'),
            charCount: document.getElementById('charCount'),
            questionGrid: document.getElementById('questionGrid'),
            
            // Loading & Modal
            loadingOverlay: document.getElementById('loadingOverlay'),
            loadingText: document.getElementById('loadingText'),
            errorModal: document.getElementById('errorModal'),
            errorMessage: document.getElementById('errorMessage')
        };
    }
    
    bindEvents() {
        // Initialize button
        this.elements.initializeBtn.addEventListener('click', () => this.initializeSystem());
        
        // Send button
        this.elements.sendBtn.addEventListener('click', () => this.sendQuestion());
        
        // Enter key in input
        this.elements.questionInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendQuestion();
            }
        });
        
        // Character count
        this.elements.questionInput.addEventListener('input', () => this.updateCharCount());
        
        // Modal close
        this.elements.closeErrorModal.addEventListener('click', () => this.hideErrorModal());
        this.elements.closeErrorBtn.addEventListener('click', () => this.hideErrorModal());
        
        // Click outside modal to close
        this.elements.errorModal.addEventListener('click', (e) => {
            if (e.target === this.elements.errorModal) {
                this.hideErrorModal();
            }
        });
    }
    
    async checkStatus() {
        try {
            const response = await fetch('/api/status');
            const data = await response.json();
            
            if (data.initialized) {
                this.isInitialized = true;
                this.updateStatus('ready', 'Sistem Hazır');
                this.showChatSection();
            } else {
                this.updateStatus('loading', 'Başlatılıyor...');
            }
        } catch (error) {
            console.error('Status check error:', error);
            this.updateStatus('error', 'Bağlantı Hatası');
        }
    }
    
    async initializeSystem() {
        if (this.isLoading) return;
        
        this.isLoading = true;
        this.showLoading('Sistem başlatılıyor...');
        this.elements.initializeBtn.disabled = true;
        
        try {
            const response = await fetch('/api/initialize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.isInitialized = true;
                this.updateStatus('ready', 'Sistem Hazır');
                this.showChatSection();
                this.showSuccessMessage('Sistem başarıyla başlatıldı!');
            } else {
                throw new Error(data.message || 'Başlatma hatası');
            }
        } catch (error) {
            console.error('Initialize error:', error);
            this.showError(error.message || 'Sistem başlatılamadı');
            this.updateStatus('error', 'Başlatma Hatası');
        } finally {
            this.isLoading = false;
            this.hideLoading();
            this.elements.initializeBtn.disabled = false;
        }
    }
    
    async sendQuestion() {
        const question = this.elements.questionInput.value.trim();
        
        if (!question || !this.isInitialized) {
            if (!this.isInitialized) {
                this.showError('Lütfen önce sistemi başlatın');
            }
            return;
        }
        
        // Add user message
        this.addMessage('user', question);
        
        // Clear input
        this.elements.questionInput.value = '';
        this.updateCharCount();
        
        // Disable send button
        this.elements.sendBtn.disabled = true;
        this.elements.questionInput.disabled = true;
        
        try {
            const response = await fetch('/api/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ question })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.addMessage('bot', data.answer, data.sources);
            } else {
                throw new Error(data.message || 'Soru cevaplanamadı');
            }
        } catch (error) {
            console.error('Ask error:', error);
            this.addMessage('bot', `Üzgünüm, bir hata oluştu: ${error.message}`);
        } finally {
            // Re-enable send button
            this.elements.sendBtn.disabled = false;
            this.elements.questionInput.disabled = false;
            this.elements.questionInput.focus();
        }
    }
    
    addMessage(type, content, sources = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = type === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        const messageText = document.createElement('p');
        messageText.textContent = content;
        messageContent.appendChild(messageText);
        
        // Add sources if available
        if (sources && sources.length > 0) {
            const sourcesDiv = document.createElement('div');
            sourcesDiv.className = 'sources';
            
            const sourcesTitle = document.createElement('h4');
            sourcesTitle.textContent = `Kaynaklar (${sources.length})`;
            sourcesDiv.appendChild(sourcesTitle);
            
            sources.forEach(source => {
                const sourceItem = document.createElement('div');
                sourceItem.className = 'source-item';
                
                let sourceText = '';
                if (source.ticker) {
                    sourceText = `Hisse: ${source.ticker}`;
                    if (source.price_change_pct !== undefined) {
                        sourceText += ` (${source.price_change_pct.toFixed(2)}%)`;
                    }
                } else if (source.coin) {
                    sourceText = `Kripto: ${source.coin}`;
                    if (source.price_change_pct !== undefined) {
                        sourceText += ` (${source.price_change_pct.toFixed(2)}%)`;
                    }
                }
                
                sourceItem.textContent = sourceText;
                sourcesDiv.appendChild(sourceItem);
            });
            
            messageContent.appendChild(sourcesDiv);
        }
        
        // Add timestamp
        const messageMeta = document.createElement('div');
        messageMeta.className = 'message-meta';
        messageMeta.textContent = new Date().toLocaleTimeString('tr-TR');
        messageContent.appendChild(messageMeta);
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageContent);
        
        this.elements.chatMessages.appendChild(messageDiv);
        this.elements.chatMessages.scrollTop = this.elements.chatMessages.scrollHeight;
        
        // Store message
        this.chatMessages.push({ type, content, sources, timestamp: new Date() });
    }
    
    async loadSampleQuestions() {
        try {
            const response = await fetch('/api/sample-questions');
            const data = await response.json();
            
            if (data.success) {
                this.elements.questionGrid.innerHTML = '';
                
                data.questions.forEach(question => {
                    const questionItem = document.createElement('div');
                    questionItem.className = 'question-item';
                    questionItem.textContent = question;
                    questionItem.addEventListener('click', () => {
                        this.elements.questionInput.value = question;
                        this.updateCharCount();
                        this.elements.questionInput.focus();
                    });
                    
                    this.elements.questionGrid.appendChild(questionItem);
                });
            }
        } catch (error) {
            console.error('Load sample questions error:', error);
        }
    }
    
    updateStatus(type, text) {
        this.elements.statusDot.className = `status-dot ${type}`;
        this.elements.statusText.textContent = text;
    }
    
    updateCharCount() {
        const count = this.elements.questionInput.value.length;
        this.elements.charCount.textContent = `${count}/500`;
        
        if (count > 450) {
            this.elements.charCount.style.color = 'var(--warning-color)';
        } else if (count > 500) {
            this.elements.charCount.style.color = 'var(--error-color)';
        } else {
            this.elements.charCount.style.color = 'var(--text-secondary)';
        }
    }
    
    showChatSection() {
        this.elements.welcomeSection.style.display = 'none';
        this.elements.chatSection.style.display = 'block';
        this.elements.questionInput.focus();
    }
    
    showLoading(text = 'Yükleniyor...') {
        this.elements.loadingText.textContent = text;
        this.elements.loadingOverlay.classList.add('show');
    }
    
    hideLoading() {
        this.elements.loadingOverlay.classList.remove('show');
    }
    
    showError(message) {
        this.elements.errorMessage.textContent = message;
        this.elements.errorModal.classList.add('show');
    }
    
    hideErrorModal() {
        this.elements.errorModal.classList.remove('show');
    }
    
    showSuccessMessage(message) {
        // Basit success notification (geliştirilebilir)
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--success-color);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: var(--radius-md);
            box-shadow: var(--shadow-lg);
            z-index: 1001;
            animation: slideIn 0.3s ease;
        `;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
}

// CSS Animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new FinanceRAGApp();
});
