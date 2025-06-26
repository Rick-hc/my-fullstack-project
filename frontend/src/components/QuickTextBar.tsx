// src/components/QuickTextBar.tsx
import React from 'react';
import {
  Box,
  Input,
  IconButton,
  useBreakpointValue,
  useColorModeValue,
} from '@chakra-ui/react';
import { FiSend } from 'react-icons/fi';
import { nanoid } from 'nanoid';
import { useRecoilState } from 'recoil';
import { inputState, messagesState } from '../store/chat';

const QuickTextBar: React.FC = () => {
  const [input, setInput] = useRecoilState(inputState);
  const [, setMessages] = useRecoilState(messagesState);

  const isMobile = useBreakpointValue({ base: true, md: false });
  const bg = useColorModeValue('white', 'gray.800');

  const handleSend = () => {
    const txt = input.trim();
    if (!txt) return;
    setMessages((prev) => [
      ...prev,
      {
        id: nanoid(),
        text: txt,
        isUser: true,      // ここが 'me'/'bot' の代わり
      },
    ]);
    setInput('');
  };

  return (
    <Box
      as="form"
      aria-label="メッセージ送信"
      onSubmit={(e) => {
        e.preventDefault();
        handleSend();
      }}
      position={isMobile ? 'fixed' : 'relative'}
      bottom={isMobile ? 0 : undefined}
      left={isMobile ? 0 : undefined}
      right={isMobile ? 0 : undefined}
      bg={bg}
      px={4}
      py={3}
      boxShadow={isMobile ? '0 -2px 8px rgba(0,0,0,0.1)' : 'none'}
      display="flex"
      alignItems="center"
      zIndex={1000}
    >
      <Input
        placeholder="メッセージを入力..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === 'Enter') {
            e.preventDefault();
            handleSend();
          }
        }}
        flex="1"
        mr={2}
      />
      <IconButton type="submit" aria-label="送信" icon={<FiSend />} />
    </Box>
  );
};

export default QuickTextBar;
