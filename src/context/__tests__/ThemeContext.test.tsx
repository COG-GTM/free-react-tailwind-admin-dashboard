import { render, screen, fireEvent, act } from '@testing-library/react';
import { ThemeProvider, useTheme } from '../ThemeContext';

const TestComponent = () => {
  const { theme, toggleTheme } = useTheme();
  return (
    <div>
      <span data-testid="theme-value">{theme}</span>
      <button onClick={toggleTheme} data-testid="toggle-button">
        Toggle Theme
      </button>
    </div>
  );
};

describe('ThemeContext', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    (localStorage.getItem as jest.Mock).mockReturnValue(null);
    (localStorage.setItem as jest.Mock).mockImplementation(() => {});
    document.documentElement.classList.remove('dark');
  });

  describe('ThemeProvider', () => {
    it('provides theme context to children', () => {
      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );
      
      expect(screen.getByTestId('theme-value')).toBeInTheDocument();
    });

    it('renders children correctly', () => {
      render(
        <ThemeProvider>
          <div data-testid="child">Child Content</div>
        </ThemeProvider>
      );
      
      expect(screen.getByTestId('child')).toBeInTheDocument();
      expect(screen.getByText('Child Content')).toBeInTheDocument();
    });

    it('defaults to light theme', async () => {
      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );
      
      await act(async () => {
        await new Promise(resolve => setTimeout(resolve, 0));
      });
      
      expect(screen.getByTestId('theme-value')).toHaveTextContent('light');
    });
  });

  describe('useTheme Hook', () => {
    it('throws error when used outside ThemeProvider', () => {
      const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
      
      expect(() => {
        render(<TestComponent />);
      }).toThrow('useTheme must be used within a ThemeProvider');
      
      consoleSpy.mockRestore();
    });

    it('returns theme and toggleTheme function', () => {
      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );
      
      expect(screen.getByTestId('theme-value')).toBeInTheDocument();
      expect(screen.getByTestId('toggle-button')).toBeInTheDocument();
    });
  });

  describe('toggleTheme', () => {
    it('toggles from light to dark', async () => {
      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );
      
      await act(async () => {
        await new Promise(resolve => setTimeout(resolve, 0));
      });
      
      expect(screen.getByTestId('theme-value')).toHaveTextContent('light');
      
      await act(async () => {
        fireEvent.click(screen.getByTestId('toggle-button'));
      });
      
      await act(async () => {
        await new Promise(resolve => setTimeout(resolve, 0));
      });
      
      expect(screen.getByTestId('theme-value')).toHaveTextContent('dark');
    });

    it('toggles from dark to light', async () => {
      (localStorage.getItem as jest.Mock).mockReturnValue('dark');
      
      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );
      
      await act(async () => {
        await new Promise(resolve => setTimeout(resolve, 0));
      });
      
      expect(screen.getByTestId('theme-value')).toHaveTextContent('dark');
      
      await act(async () => {
        fireEvent.click(screen.getByTestId('toggle-button'));
      });
      
      await act(async () => {
        await new Promise(resolve => setTimeout(resolve, 0));
      });
      
      expect(screen.getByTestId('theme-value')).toHaveTextContent('light');
    });

    it('toggles multiple times correctly', async () => {
      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );
      
      await act(async () => {
        await new Promise(resolve => setTimeout(resolve, 0));
      });
      
      expect(screen.getByTestId('theme-value')).toHaveTextContent('light');
      
      await act(async () => {
        fireEvent.click(screen.getByTestId('toggle-button'));
      });
      
      await act(async () => {
        await new Promise(resolve => setTimeout(resolve, 0));
      });
      
      expect(screen.getByTestId('theme-value')).toHaveTextContent('dark');
      
      await act(async () => {
        fireEvent.click(screen.getByTestId('toggle-button'));
      });
      
      await act(async () => {
        await new Promise(resolve => setTimeout(resolve, 0));
      });
      
      expect(screen.getByTestId('theme-value')).toHaveTextContent('light');
    });
  });

  describe('localStorage Integration', () => {
    it('reads saved theme from localStorage', async () => {
      (localStorage.getItem as jest.Mock).mockReturnValue('dark');
      
      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );
      
      await act(async () => {
        await new Promise(resolve => setTimeout(resolve, 0));
      });
      
      expect(localStorage.getItem).toHaveBeenCalledWith('theme');
      expect(screen.getByTestId('theme-value')).toHaveTextContent('dark');
    });

    it('saves theme to localStorage when toggled', async () => {
      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );
      
      await act(async () => {
        await new Promise(resolve => setTimeout(resolve, 0));
      });
      
      await act(async () => {
        fireEvent.click(screen.getByTestId('toggle-button'));
      });
      
      await act(async () => {
        await new Promise(resolve => setTimeout(resolve, 0));
      });
      
      expect(localStorage.setItem).toHaveBeenCalledWith('theme', 'dark');
    });

    it('defaults to light when localStorage is empty', async () => {
      (localStorage.getItem as jest.Mock).mockReturnValue(null);
      
      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );
      
      await act(async () => {
        await new Promise(resolve => setTimeout(resolve, 0));
      });
      
      expect(screen.getByTestId('theme-value')).toHaveTextContent('light');
    });
  });

  describe('DOM Class Management', () => {
    it('adds dark class to documentElement when theme is dark', async () => {
      (localStorage.getItem as jest.Mock).mockReturnValue('dark');
      
      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );
      
      await act(async () => {
        await new Promise(resolve => setTimeout(resolve, 0));
      });
      
      expect(document.documentElement.classList.contains('dark')).toBe(true);
    });

    it('removes dark class from documentElement when theme is light', async () => {
      document.documentElement.classList.add('dark');
      (localStorage.getItem as jest.Mock).mockReturnValue('light');
      
      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );
      
      await act(async () => {
        await new Promise(resolve => setTimeout(resolve, 0));
      });
      
      expect(document.documentElement.classList.contains('dark')).toBe(false);
    });
  });
});
