import React from 'react';
import { Avatar, Box, HStack, Text, useColorModeValue } from '@chakra-ui/react';
import { motion } from 'framer-motion';

interface MessageBubbleProps {
  sender: 'user' | 'bot';
  message: string;
}

const MotionBox = motion(Box);

/**
 * MessageBubble – v4 (photo avatars)
 * ----------------------------------
 * • ユーザー: 指定の写真 URL
 * • Bot: 指定の写真 URL
 * • Fallback: 背景色とイニシャル
 */
const MessageBubble: React.FC<MessageBubbleProps> = ({ sender, message }) => {
  const isUser = sender === 'user';

  // Bubble colours (WCAG AA)
  const bubbleBg = useColorModeValue(
    isUser ? 'blue.600' : 'gray.100',
    isUser ? 'blue.500' : 'gray.700'
  );
  const textColor = useColorModeValue(isUser ? 'white' : 'gray.800', 'white');

  // Avatar props (images provided by user)
  const avatarProps = isUser
    ? {
        src: 'https://sdmntpreastus.oaiusercontent.com/files/00000000-20d8-61f9-9864-7ab829138a06/raw?se=2025-06-24T05%3A16%3A34Z&sp=r&sv=2024-08-04&sr=b&scid=dde1257b-ba51-5587-a2df-bd33ad1f147c&skoid=b0fd38cc-3d33-418f-920e-4798de4acdd1&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-06-24T04%3A46%3A02Z&ske=2025-06-25T04%3A46%3A02Z&sks=b&skv=2024-08-04&sig=DdhAkmKy4zHqNfqOMLAPQAhN58meJiJ20ljhpkjIKe8%3D',
        name: 'Me',
      }
    : {
        src: 'https://sdmntpreastus.oaiusercontent.com/files/00000000-93a4-61f9-8811-8c07725bdc8d/raw?se=2025-06-24T06%3A05%3A12Z&sp=r&sv=2024-08-04&sr=b&scid=56dc14c0-bcd2-5b9b-b6a7-020ad78c3aa8&skoid=b0fd38cc-3d33-418f-920e-4798de4acdd1&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-06-23T21%3A24%3A00Z&ske=2025-06-24T21%3A24%3A00Z&sks=b&skv=2024-08-04&sig=ULPLNj1/1KLoQ95jL0fvp/a7ca9l95AZ0I9djPQwNQI%3D',
        name: 'Bot',
      };

  return (
    <HStack
      alignSelf={isUser ? 'flex-end' : 'flex-start'}
      spacing={3}
      my={1.5}
      flexDir={isUser ? 'row-reverse' : 'row'}
      maxW="80%"
      role="group"
      tabIndex={0}
      _focusVisible={{ boxShadow: 'outline' }}
    >
      <Avatar size="sm" {...avatarProps} />

      <MotionBox
        px={4}
        py={3}
        bg={bubbleBg}
        color={textColor}
        borderRadius="2xl"
        boxShadow="xs"
        whiteSpace="pre-wrap"
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.18 }}
      >
        <Text fontSize="sm" lineHeight="1.6">
          {message}
        </Text>
      </MotionBox>
    </HStack>
  );
};

export default MessageBubble;
