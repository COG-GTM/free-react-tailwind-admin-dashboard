import { render, screen, fireEvent } from '@testing-library/react';
import Button from '../ui/button/Button';

describe('Button Component', () => {
  describe('Rendering', () => {
    it('renders children correctly', () => {
      render(<Button>Click me</Button>);
      expect(screen.getByText('Click me')).toBeInTheDocument();
    });

    it('renders as a button element', () => {
      render(<Button>Test</Button>);
      expect(screen.getByRole('button')).toBeInTheDocument();
    });
  });

  describe('Sizes', () => {
    it('applies small size classes', () => {
      render(<Button size="sm">Small Button</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveClass('px-4', 'py-3', 'text-sm');
    });

    it('applies medium size classes by default', () => {
      render(<Button>Medium Button</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveClass('px-5', 'py-3.5', 'text-sm');
    });
  });

  describe('Variants', () => {
    it('applies primary variant classes by default', () => {
      render(<Button>Primary Button</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveClass('bg-brand-500', 'text-white');
    });

    it('applies outline variant classes', () => {
      render(<Button variant="outline">Outline Button</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveClass('bg-white', 'text-gray-700');
    });
  });

  describe('Icons', () => {
    it('renders start icon when provided', () => {
      const StartIcon = () => <span data-testid="start-icon">Start</span>;
      render(<Button startIcon={<StartIcon />}>With Start Icon</Button>);
      expect(screen.getByTestId('start-icon')).toBeInTheDocument();
    });

    it('renders end icon when provided', () => {
      const EndIcon = () => <span data-testid="end-icon">End</span>;
      render(<Button endIcon={<EndIcon />}>With End Icon</Button>);
      expect(screen.getByTestId('end-icon')).toBeInTheDocument();
    });

    it('renders both icons when provided', () => {
      const StartIcon = () => <span data-testid="start-icon">Start</span>;
      const EndIcon = () => <span data-testid="end-icon">End</span>;
      render(
        <Button startIcon={<StartIcon />} endIcon={<EndIcon />}>
          With Both Icons
        </Button>
      );
      expect(screen.getByTestId('start-icon')).toBeInTheDocument();
      expect(screen.getByTestId('end-icon')).toBeInTheDocument();
    });
  });

  describe('Click Handler', () => {
    it('calls onClick when clicked', () => {
      const handleClick = jest.fn();
      render(<Button onClick={handleClick}>Clickable</Button>);
      
      fireEvent.click(screen.getByRole('button'));
      expect(handleClick).toHaveBeenCalledTimes(1);
    });

    it('does not call onClick when disabled', () => {
      const handleClick = jest.fn();
      render(
        <Button onClick={handleClick} disabled>
          Disabled
        </Button>
      );
      
      fireEvent.click(screen.getByRole('button'));
      expect(handleClick).not.toHaveBeenCalled();
    });
  });

  describe('Disabled State', () => {
    it('applies disabled attribute when disabled', () => {
      render(<Button disabled>Disabled Button</Button>);
      expect(screen.getByRole('button')).toBeDisabled();
    });

    it('applies disabled styles when disabled', () => {
      render(<Button disabled>Disabled Button</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveClass('cursor-not-allowed', 'opacity-50');
    });

    it('is not disabled by default', () => {
      render(<Button>Enabled Button</Button>);
      expect(screen.getByRole('button')).not.toBeDisabled();
    });
  });

  describe('Custom className', () => {
    it('applies custom className', () => {
      render(<Button className="custom-class">Custom</Button>);
      expect(screen.getByRole('button')).toHaveClass('custom-class');
    });

    it('merges custom className with default classes', () => {
      render(<Button className="custom-class">Custom</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveClass('custom-class');
      expect(button).toHaveClass('inline-flex');
    });
  });
});
