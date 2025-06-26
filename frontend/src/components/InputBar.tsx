import React, { useEffect, useRef, useState } from 'react';
import {
  HStack,
  IconButton,
  Textarea,
  useColorModeValue,
} from '@chakra-ui/react';
import { FiSend } from 'react-icons/fi';

// -----------------------------------------------------------------------------
// Props
// -----------------------------------------------------------------------------
interface InputBarProps {
  onSend: (message: string) => void;
}

/**
 * Reusable chat input bar.
 *
 * - Auto-resizing <textarea>
 * - Enter = send / Shift+Enter = newline
 * - Disabled send button while empty
 *
 * No business logic – purely UI.
 */
export const InputBar: React.FC<InputBarProps> = ({ onSend }) => {
  const [value, setValue] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement | null>(null);

  // ---------------------------------------------------------------------------
  // Auto-resize textarea height
  // ---------------------------------------------------------------------------
  useEffect(() => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = 'auto';
    el.style.height = `${el.scrollHeight}px`;
  }, [value]);

  // ---------------------------------------------------------------------------
  // Helpers
  // ---------------------------------------------------------------------------
  const handleSend = () => {
    if (!value.trim()) return;
    onSend(value.trim());
    setValue('');
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // ---------------------------------------------------------------------------
  // Render
  // ---------------------------------------------------------------------------
  return (
    <HStack
      spacing={2}
      p={4}
      borderTopWidth="1px"
      bg={useColorModeValue('white', 'gray.800')}
    >
      <Textarea
        ref={textareaRef}
        value={value}
        placeholder="質問を入力…"
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={handleKeyDown}
        resize="none"
        rows={1}
        maxH="160px"
        flex="1"
        fontSize="sm"
        lineHeight="1.4"
      />
      <IconButton
        aria-label="送信"
        icon={<FiSend />}
        colorScheme="blue"
        onClick={handleSend}
        isDisabled={!value.trim()}
      />
    </HStack>
  );
};

export default InputBar;
