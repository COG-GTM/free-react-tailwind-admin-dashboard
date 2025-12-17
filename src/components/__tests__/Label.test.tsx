import { render, screen } from '@testing-library/react';
import Label from '../form/Label';

describe('Label Component', () => {
  describe('Rendering', () => {
    it('renders children correctly', () => {
      render(<Label>Email Address</Label>);
      expect(screen.getByText('Email Address')).toBeInTheDocument();
    });

    it('renders as a label element', () => {
      render(<Label>Test Label</Label>);
      const label = screen.getByText('Test Label');
      expect(label.tagName).toBe('LABEL');
    });
  });

  describe('htmlFor attribute', () => {
    it('applies htmlFor attribute when provided', () => {
      render(<Label htmlFor="email-input">Email</Label>);
      const label = screen.getByText('Email');
      expect(label).toHaveAttribute('for', 'email-input');
    });

    it('does not have htmlFor when not provided', () => {
      render(<Label>No For</Label>);
      const label = screen.getByText('No For');
      expect(label).not.toHaveAttribute('for');
    });
  });

  describe('Styling', () => {
    it('applies default styling classes', () => {
      render(<Label>Styled Label</Label>);
      const label = screen.getByText('Styled Label');
      expect(label).toHaveClass('mb-1.5', 'block', 'text-sm', 'font-medium');
    });

    it('applies custom className', () => {
      render(<Label className="custom-label-class">Custom</Label>);
      const label = screen.getByText('Custom');
      expect(label).toHaveClass('custom-label-class');
    });

    it('merges custom className with default classes', () => {
      render(<Label className="extra-margin">Merged</Label>);
      const label = screen.getByText('Merged');
      expect(label).toHaveClass('extra-margin');
      expect(label).toHaveClass('block');
    });
  });

  describe('Children types', () => {
    it('renders string children', () => {
      render(<Label>String Child</Label>);
      expect(screen.getByText('String Child')).toBeInTheDocument();
    });

    it('renders element children', () => {
      render(
        <Label>
          <span data-testid="child-span">Span Child</span>
        </Label>
      );
      expect(screen.getByTestId('child-span')).toBeInTheDocument();
    });

    it('renders multiple children', () => {
      render(
        <Label>
          Required Field <span>*</span>
        </Label>
      );
      expect(screen.getByText(/Required Field/)).toBeInTheDocument();
    });
  });

  describe('Accessibility', () => {
    it('associates label with input via htmlFor', () => {
      const { container } = render(
        <div>
          <Label htmlFor="test-input">Test Input</Label>
          <input id="test-input" type="text" />
        </div>
      );
      
      const label = screen.getByText('Test Input');
      const input = container.querySelector('#test-input');
      
      expect(label).toHaveAttribute('for', 'test-input');
      expect(input).toHaveAttribute('id', 'test-input');
    });
  });
});
