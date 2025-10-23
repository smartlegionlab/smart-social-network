class IndicatorSocket {
  constructor(url) {
    if (!IndicatorSocket.instance) {
      this.url = url;
      this.socket = null;
      this.reconnectAttempts = 0;
      this.maxReconnectAttempts = 5;
      this.reconnectDelay = 1000;

      this.notificationConfig = {
        unread_messages: {
          iconId: 'new_msg_icon',
          dotContainerId: 'message_count',
          iconClasses: ['bi-envelope', 'bi-envelope-fill'],
          dotId: 'new_msg_dot'
        },
        new_views: {
          iconId: 'view_icon',
          dotContainerId: 'profile_view_count',
          iconClasses: ['bi-eye', 'bi-eye-fill'],
          dotId: 'view_dot'
        },
        friend_requests: {
          iconId: 'new_friend_icon',
          dotContainerId: 'new_friend_count',
          iconClasses: ['bi-people', 'bi-people-fill'],
          dotId: 'new_friend_dot'
        },
        new_posts: {
          iconId: 'new_post_icon',
          dotContainerId: 'new_post_count',
          iconClasses: ['bi-house-door', 'bi-house-door-fill'],
          dotId: 'new_post_dot'
        },
        notifications: {
          iconId: 'notification_icon',
          dotContainerId: 'profile_notification_count',
          iconClasses: ['bi-bell', 'bi-bell-fill'],
          dotId: 'notification_dot'
        }
      };

      if (window.isAuthenticated) {
        this.connect();
      }

      IndicatorSocket.instance = this;
    }
    return IndicatorSocket.instance;
  }

  connect() {
    if (this.socket?.readyState === WebSocket.OPEN) return;

    this.socket = new WebSocket(this.url);

    this.socket.onopen = () => {
      this.reconnectAttempts = 0;
      this.reconnectDelay = 1000;
    };

    this.socket.onmessage = (event) => this.handleMessage(event);
    this.socket.onclose = (event) => this.handleClose(event);
    this.socket.onerror = (error) => {
      console.error('WebSocket error:', error);
      this.socket.close();
    };
  }

  handleMessage(event) {
    try {
      const data = JSON.parse(event.data);

      if (data.has_unread_messages !== undefined) {
        this.updateUI('unread_messages', data.has_unread_messages);
      }
      if (data.has_new_views !== undefined) {
        this.updateUI('new_views', data.has_new_views);
      }
      if (data.has_friend_requests !== undefined) {
        this.updateUI('friend_requests', data.has_friend_requests);
      }
      if (data.has_new_posts !== undefined) {
        this.updateUI('new_posts', data.has_new_posts);
      }
      if (data.has_notifications !== undefined) {
        this.updateUI('notifications', data.has_notifications);
      }

    } catch (error) {
      console.error('Error processing message:', error);
    }
  }

  updateUI(type, isActive) {
    const config = this.notificationConfig[type];
    if (!config) return;

    const icon = document.getElementById(config.iconId);
    const container = document.getElementById(config.dotContainerId);

    if (!icon || !container) {
      console.warn(`Elements not found for ${type} notification`);
      return;
    }

    icon.classList.toggle(config.iconClasses[0], !isActive);
    icon.classList.toggle(config.iconClasses[1], isActive);

    let dot = document.getElementById(config.dotId);
    if (isActive) {
      if (!dot) {
        dot = document.createElement('i');
        dot.id = config.dotId;
        dot.className = 'bi bi-circle-fill';
        dot.style.cssText = 'font-size:0.6em; width:7px;';
        container.appendChild(dot);
      }
    } else if (dot) {
      dot.remove();
    }
  }

  handleClose(event) {
    if (event.code !== 1000) {
      this.handleReconnect();
    }
  }

  handleReconnect() {
    if (!window.isAuthenticated || this.reconnectAttempts >= this.maxReconnectAttempts) {
      return;
    }

    this.reconnectAttempts++;
    setTimeout(() => this.connect(), this.reconnectDelay);
    this.reconnectDelay *= 2;
  }
}

const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
const websocketInstance = window.isAuthenticated
  ? new IndicatorSocket(`${protocol}//${window.location.host}/ws/counters/`)
  : null;

export default websocketInstance;