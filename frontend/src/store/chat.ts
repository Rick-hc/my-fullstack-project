// src/store/chat.ts
import { atom } from 'recoil';

// 送受信されたメッセージ一覧
export interface Message {
  id: string;
  text: string;
  from: 'user' | 'bot';
}

export const messagesState = atom<Message[]>({
  key: 'messagesState',
  default: [],  // 初期は空配列
});

// 入力フォームの現在の文字列
export const inputState = atom<string>({
  key: 'inputState',
  default: '',  // 初期は空文字
});
