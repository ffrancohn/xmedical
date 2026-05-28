import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react'
import { Theme } from '@/types'

interface ThemeContextType {
  theme: Theme
  setTheme: (theme: Theme) => void
  toggleMode: () => void
  setColor: (color: Theme['color']) => void
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined)

interface ThemeProviderProps {
  children: ReactNode
}

const defaultTheme: Theme = {
  mode: 'light',
  color: 'blue'
}

export const ThemeProvider: React.FC<ThemeProviderProps> = ({ children }) => {
  const [theme, setThemeState] = useState<Theme>(() => {
    // Intentar recuperar tema del localStorage
    const savedTheme = localStorage.getItem('xmedical-theme')
    if (savedTheme) {
      try {
        return JSON.parse(savedTheme)
      } catch {
        return defaultTheme
      }
    }
    return defaultTheme
  })

  // Guardar tema en localStorage cuando cambie
  useEffect(() => {
    localStorage.setItem('xmedical-theme', JSON.stringify(theme))
    
    // Aplicar tema al documento
    document.documentElement.setAttribute('data-theme', theme.mode)
    document.documentElement.setAttribute('data-color', theme.color)
    
    // Aplicar clases de Bootstrap para modo oscuro
    if (theme.mode === 'dark') {
      document.body.classList.add('bg-dark', 'text-light')
    } else {
      document.body.classList.remove('bg-dark', 'text-light')
    }
  }, [theme])

  const setTheme = (newTheme: Theme) => {
    setThemeState(newTheme)
  }

  const toggleMode = () => {
    setThemeState(prev => ({
      ...prev,
      mode: prev.mode === 'light' ? 'dark' : 'light'
    }))
  }

  const setColor = (color: Theme['color']) => {
    setThemeState(prev => ({
      ...prev,
      color
    }))
  }

  const value: ThemeContextType = {
    theme,
    setTheme,
    toggleMode,
    setColor,
  }

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  )
}

export const useTheme = (): ThemeContextType => {
  const context = useContext(ThemeContext)
  if (context === undefined) {
    throw new Error('useTheme debe ser usado dentro de un ThemeProvider')
  }
  return context
} 