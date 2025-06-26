import React, { useState } from 'react';
import {
  Box,
  Flex,
  HStack,
  IconButton,
  Input,
  useColorModeValue,
} from '@chakra-ui/react';
import { FiSend } from 'react-icons/fi';
import { sendQuery } from '../api/chat';
import TypingIndicator from './TypingIndicator';
import MessageBubble from './MessageBubble';
import { useChatScroll } from '../hooks/useChatScroll';

// -----------------------------------------------------------------------------
// Types
// -----------------------------------------------------------------------------
interface ChatMessage {
  from: 'user' | 'bot';
  text: string;
}

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
const ChatWindow: React.FC = () => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isBotTyping, setIsBotTyping] = useState(false);

  // Auto-scroll hook (bottomRef is attached after message list)
  const { bottomRef } = useChatScroll<HTMLDivElement>([
    messages.length,
    isBotTyping,
  ]);

  // ---------------------------------------------------------------------------
  // Handlers
  // ---------------------------------------------------------------------------
  const handleSend = async () => {
    const question = input.trim();
    if (!question) return;

    // ユーザーメッセージを追加
    setMessages((prev) => [...prev, { from: 'user', text: question }]);
    setInput('');

    // タイピングインジケーター ON
    setIsBotTyping(true);

    try {
      const reply = await sendQuery(question);
      setMessages((prev) => [...prev, { from: 'bot', text: reply }]);
    } catch (e) {
      console.error(e);
      setMessages((prev) => [
        ...prev,
        { from: 'bot', text: '通信エラーが発生しました。' },
      ]);
    } finally {
      // タイピングインジケーター OFF
      setIsBotTyping(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // ---------------------------------------------------------------------------
  // Render
  // ---------------------------------------------------------------------------
  return (
    <Flex direction="column" h="full" maxH="100vh" overflow="hidden">
      {/* Message list */}
      <Flex
        direction="column"
        flex="1"
        overflowY="auto"
        px={{ base: 3, md: 4 }}
        pt={4}
      >
        {messages.map((m, i) => (
          <MessageBubble
            key={`${m.from}-${i}`}
            sender={m.from === 'user' ? 'user' : 'bot'}
            message={m.text}
          />
        ))}

        {/* Bot is typing… */}
        {isBotTyping && <TypingIndicator />}

        {/* Dummy div for auto-scroll */}
        <div ref={bottomRef} />
      </Flex>

      {/* Input area */}
      <HStack
        p={4}
        spacing={2}
        borderTopWidth="1px"
        bg={useColorModeValue('white', 'gray.800')}
      >
        <Input
          flex="1"
          value={input}
          placeholder="質問を入力…"
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <IconButton
          aria-label="送信"
          icon={<FiSend />}
          onClick={handleSend}
          colorScheme="blue"
          isDisabled={!input.trim()}
        />
      </HStack>
    </Flex>
  );
};

export default ChatWindow;
