import { renderHook, act } from '@testing-library/react';
import { useModal } from '../useModal';

describe('useModal Hook', () => {
  describe('Initial State', () => {
    it('starts with isOpen as false by default', () => {
      const { result } = renderHook(() => useModal());
      expect(result.current.isOpen).toBe(false);
    });

    it('starts with isOpen as true when initialState is true', () => {
      const { result } = renderHook(() => useModal(true));
      expect(result.current.isOpen).toBe(true);
    });

    it('starts with isOpen as false when initialState is false', () => {
      const { result } = renderHook(() => useModal(false));
      expect(result.current.isOpen).toBe(false);
    });
  });

  describe('openModal', () => {
    it('sets isOpen to true', () => {
      const { result } = renderHook(() => useModal());
      
      act(() => {
        result.current.openModal();
      });
      
      expect(result.current.isOpen).toBe(true);
    });

    it('keeps isOpen as true when already open', () => {
      const { result } = renderHook(() => useModal(true));
      
      act(() => {
        result.current.openModal();
      });
      
      expect(result.current.isOpen).toBe(true);
    });
  });

  describe('closeModal', () => {
    it('sets isOpen to false', () => {
      const { result } = renderHook(() => useModal(true));
      
      act(() => {
        result.current.closeModal();
      });
      
      expect(result.current.isOpen).toBe(false);
    });

    it('keeps isOpen as false when already closed', () => {
      const { result } = renderHook(() => useModal(false));
      
      act(() => {
        result.current.closeModal();
      });
      
      expect(result.current.isOpen).toBe(false);
    });
  });

  describe('toggleModal', () => {
    it('toggles isOpen from false to true', () => {
      const { result } = renderHook(() => useModal(false));
      
      act(() => {
        result.current.toggleModal();
      });
      
      expect(result.current.isOpen).toBe(true);
    });

    it('toggles isOpen from true to false', () => {
      const { result } = renderHook(() => useModal(true));
      
      act(() => {
        result.current.toggleModal();
      });
      
      expect(result.current.isOpen).toBe(false);
    });

    it('toggles multiple times correctly', () => {
      const { result } = renderHook(() => useModal(false));
      
      act(() => {
        result.current.toggleModal();
      });
      expect(result.current.isOpen).toBe(true);
      
      act(() => {
        result.current.toggleModal();
      });
      expect(result.current.isOpen).toBe(false);
      
      act(() => {
        result.current.toggleModal();
      });
      expect(result.current.isOpen).toBe(true);
    });
  });

  describe('Function Stability', () => {
    it('returns stable function references', () => {
      const { result, rerender } = renderHook(() => useModal());
      
      const initialOpenModal = result.current.openModal;
      const initialCloseModal = result.current.closeModal;
      const initialToggleModal = result.current.toggleModal;
      
      rerender();
      
      expect(result.current.openModal).toBe(initialOpenModal);
      expect(result.current.closeModal).toBe(initialCloseModal);
      expect(result.current.toggleModal).toBe(initialToggleModal);
    });
  });

  describe('Return Value Structure', () => {
    it('returns an object with isOpen, openModal, closeModal, and toggleModal', () => {
      const { result } = renderHook(() => useModal());
      
      expect(result.current).toHaveProperty('isOpen');
      expect(result.current).toHaveProperty('openModal');
      expect(result.current).toHaveProperty('closeModal');
      expect(result.current).toHaveProperty('toggleModal');
    });

    it('returns functions for openModal, closeModal, and toggleModal', () => {
      const { result } = renderHook(() => useModal());
      
      expect(typeof result.current.openModal).toBe('function');
      expect(typeof result.current.closeModal).toBe('function');
      expect(typeof result.current.toggleModal).toBe('function');
    });

    it('returns boolean for isOpen', () => {
      const { result } = renderHook(() => useModal());
      expect(typeof result.current.isOpen).toBe('boolean');
    });
  });
});
