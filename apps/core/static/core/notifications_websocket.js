class NotificationManager {
    constructor() {
        this.socket = null;
        this.initialize();
    }

    initialize() {
        if (!window.isAuthenticated) return;

        const wsScheme = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
        this.socket = new WebSocket(`${wsScheme}${window.location.host}/ws/notifications/`);

        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.showNotification(data);
        };

        this.socket.onclose = () => {
            setTimeout(() => this.initialize(), 5000);
        };
    }

    showNotification(notification) {
        const container = document.getElementById('toast-container');
        if (!container) return;

        const iconMap = {
            'new_message': 'bi-chat-text',
            'friend_request': 'bi-people',
            'user_view': 'bi-eye',
            'post_like': 'bi-heart',
            'post_comment': 'bi-chat'
        };

        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.innerHTML = `
            <div class="toast-header bg-primary text-white">
                <i class="bi ${iconMap[notification.type] || 'bi-bell'} me-2"></i>
                <strong class="me-auto">${notification.type.replace(/_/g, ' ')}</strong>
                <small class="text-white">${notification.time_since}</small>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${notification.message}
                ${notification.sender ? `
                <div class="mt-2 d-flex align-items-center">
                    <img src="${notification.sender.avatar}" 
                         class="rounded-circle object-fit-cover me-2" 
                         width="24" 
                         height="24">
                    <small>${notification.sender.name}</small>
                </div>
                ` : ''}
            </div>
        `;

        container.appendChild(toast);
        new bootstrap.Toast(toast, { autohide: true, delay: 5000 }).show();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    if (window.isAuthenticated) {
        new NotificationManager();
    }
});