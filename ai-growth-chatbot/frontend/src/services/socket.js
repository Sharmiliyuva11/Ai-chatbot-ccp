import { io } from 'socket.io-client';

const SOCKET_URL = 'http://localhost:5000';

class SocketService {
  constructor() {
    this.socket = null;
  }

  connect(token) {
    if (this.socket && this.socket.connected) return this.socket;

    const opts = {
      transports: ['websocket'],
      // Pass token in query so backend can decode it on connect
      query: {
        token: token || ''
      },
      reconnectionAttempts: 5,
      reconnectionDelay: 1000
    };

    this.socket = io(SOCKET_URL, opts);

    this.socket.on('connect', () => {
      console.log('🔌 Socket connected', this.socket.id);
    });

    this.socket.on('disconnect', (reason) => {
      console.log('🔌 Socket disconnected', reason);
    });

    return this.socket;
  }

  on(event, cb) {
    if (!this.socket) return;
    this.socket.on(event, cb);
  }

  off(event, cb) {
    if (!this.socket) return;
    this.socket.off(event, cb);
  }

  emit(event, data) {
    if (!this.socket) return;
    this.socket.emit(event, data);
  }

  joinUserRoom(userId) {
    if (!this.socket) return;
    this.socket.emit('join_user_room', { userId });
  }
}

export default new SocketService();
