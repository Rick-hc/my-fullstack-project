import React from 'react';
import { HStack, Text, useColorModeValue } from '@chakra-ui/react';
import { motion } from 'framer-motion';

/**
 * TypingIndicator – v2
 * --------------------
 * より視認性を高めた「Botが入力中…」インジケーター。
 * • 先頭にテキスト “Botが入力中”
 * • ドット 3 個は拡大縮小 + フェードでバウンス
 * • アクセシビリティ: role="status" aria-live="polite"
 */

const Dot = motion(Text);

const TypingIndicator: React.FC = () => {
  const dotColor = useColorModeValue('gray.500', 'gray.400');

  return (
    <HStack
      alignSelf="flex-start"
      spacing={1}
      px={4}
      py={2}
      role="status"
      aria-live="polite"
    >
      {/* Text label */}
      <Text fontSize="sm" color={dotColor} pr={1}>
        Botが入力中
      </Text>

      {/* Animated dots */}
      {Array.from({ length: 3 }).map((_, i) => (
        <Dot
          key={i}
          fontSize="xl"
          lineHeight="1"
          color={dotColor}
          initial={{ opacity: 0.3, scale: 0.5 }}
          animate={{ opacity: [0.3, 1, 0.3], scale: [0.5, 1, 0.5] }}
          transition={{ repeat: Infinity, duration: 1.2, delay: i * 0.2 }}
        >
          ·
        </Dot>
      ))}
    </HStack>
  );
};

export default TypingIndicator;
