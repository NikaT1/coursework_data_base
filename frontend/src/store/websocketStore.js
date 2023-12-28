import { reactive } from "vue";
import SockJS from "sockjs-client";
import Stomp from "webstomp-client";

const state = reactive({
  socket: null,
  stompClient: null,
  isConnected: false,
});

function connect() {
  if (!state.isConnected) {
    state.socket = new SockJS("/localhost:8080");
    state.stompClient = Stomp.over(state.socket);
    state.stompClient.connect(
      {},
        (frame) => {
            console.log(frame);
        state.isConnected = true;
      },
        (error) => {
            console.log(error);
        state.isConnected = false;
      }
    );
  }
}

function disconnect() {
  if (state.isConnected) {
    state.stompClient.disconnect(() => {
      state.isConnected = false;
      state.stompClient = null;
      state.socket = null;
    });
  }
}

function subscribe(topic, callback) {
  if (state.isConnected) {
    state.stompClient.subscribe(topic, callback);
  }
}

function send(destination, headers = {}, body = "") {
  if (state.isConnected) {
    state.stompClient.send(destination, headers, body);
  }
}

export default {
  state,
  connect,
  disconnect,
  subscribe,
  send,
};