/**
 * Hook: useChatScroll
 * -------------------
 * Provides a `bottomRef` to attach at the end of your chat list and a
 * `scrollToBottom` helper. Whenever any dependency in `deps` changes, the
 * hook triggers a smooth scroll to the referenced element, ensuring the latest
 * message is always visible.
 *
 * Example usage:
 * ```tsx
 * const { bottomRef, scrollToBottom } = useChatScroll([messages.length]);
 * ...
 * <div ref={bottomRef} />
 * ```
 */
import { useEffect, useRef } from 'react';

export function useChatScroll<T extends HTMLElement>(
  /** Dependencies that should trigger auto‑scroll (e.g., `messages.length`) */
  deps: React.DependencyList = []
) {
  const bottomRef = useRef<T | null>(null);

  /** Smoothly scrolls to the bottom element. */
  const scrollToBottom = (behavior: ScrollBehavior = 'smooth') => {
    bottomRef.current?.scrollIntoView({ behavior });
  };

  // Auto‑scroll when dependencies change
  useEffect(() => {
    scrollToBottom('auto');
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  return { bottomRef, scrollToBottom } as const;
}
