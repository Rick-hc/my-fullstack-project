import React from 'react';
import {
  chakra,
  Flex,
  FlexProps,
  Heading,
  IconButton,
  Button,
  useColorMode,
  useColorModeValue,
  VisuallyHidden,
} from '@chakra-ui/react';
import { FiSun, FiMoon, FiPlusCircle } from 'react-icons/fi';
import { motion } from 'framer-motion';
import { useSetRecoilState } from 'recoil';
import { messagesState, inputState } from '../store/chat';

// Motion‑enabled Chakra Flex with proper typings
const MotionFlex = motion<FlexProps>(Flex);

// Framer‑Motion spring preset (optional)
const spring = {
  type: 'spring',
  damping: 10,
  stiffness: 100,
};

/**
 * Sticky, animated header.
 * UI‑only enhancement – original behaviour preserved.
 */
const Header: React.FC = () => {
  const { colorMode, toggleColorMode } = useColorMode();
  const gradient = useColorModeValue(
    'linear(to-r, teal.300, blue.400)',
    'linear(to-r, teal.500, blue.600)'
  );

  const setMessages = useSetRecoilState(messagesState);
  const setInput = useSetRecoilState(inputState);

  const startNewChat = () => {
    setMessages([]);
    setInput('');
  };

  return (
    <>
      {/* Skip link for accessibility */}
      <chakra.a
        href="#main"
        position="absolute"
        top="-40px"
        left="0"
        _focus={{ top: 0 }}
        bg="gray.800"
        color="white"
        p={2}
        zIndex="skipLink"
      >
        Skip to content
      </chakra.a>

      <MotionFlex
        as="header"
        align="center"
        w="full"
        px={{ base: 4, md: 6 }}
        py={3}
        bgGradient={gradient}
        boxShadow="sm"
        position="sticky"
        top={0}
        zIndex="banner"
        initial={{ y: -16, opacity: 0 }}
        animate={{ y: 0, opacity: 1, transition: spring }}
      >
        {/* Brand */}
        <Heading
          as="h1"
          id="site-title"
          size="md"
          color="white"
          letterSpacing="tight"
        >
          ChatBot&nbsp;UI&nbsp;
          <chakra.span fontSize="sm" fontWeight="normal" opacity={0.8}>
            (Beta)
          </chakra.span>
        </Heading>

        {/* Actions */}
        <Flex ml="auto" align="center" gap={2}>
          <Button
            size="sm"
            leftIcon={<FiPlusCircle />}
            bgGradient="linear(to-r, pink.400, pink.600)"
            _hover={{ filter: 'brightness(1.05)' }}
            _active={{ filter: 'brightness(0.95)' }}
            color="white"
            onClick={startNewChat}
            aria-label="Start new chat"
            whiteSpace="nowrap"
          >
            新規チャット
          </Button>

          <IconButton
            size="sm"
            aria-label="Toggle color mode"
            variant="ghost"
            color="white"
            onClick={toggleColorMode}
            icon={colorMode === 'light' ? <FiMoon /> : <FiSun />}
            _focusVisible={{ boxShadow: 'outline' }}
          >
            <VisuallyHidden>カラーモード切替</VisuallyHidden>
          </IconButton>
        </Flex>
      </MotionFlex>
    </>
  );
};

export default Header;
