/**
 * Style Dictionary Configuration
 * 
 * Transforms DTCG format tokens to platform-specific outputs.
 * 
 * Usage:
 *   npx style-dictionary build --config style-dictionary.config.js
 * 
 * For DTCG format support, install @tokens-studio/sd-transforms:
 *   npm install @tokens-studio/sd-transforms
 */

import { register } from '@tokens-studio/sd-transforms';
import StyleDictionary from 'style-dictionary';

// Register DTCG transforms
register(StyleDictionary);

// Define themes (add more as needed)
const themes = ['light', 'dark'];

// Define platforms (add more as needed)
const platforms = {
  // CSS Custom Properties
  css: {
    transformGroup: 'tokens-studio',
    buildPath: 'build/css/',
    files: [{
      destination: 'variables.css',
      format: 'css/variables',
      options: {
        outputReferences: true,  // Preserve aliases as var()
        selector: ':root'
      }
    }]
  },

  // Sass Variables
  scss: {
    transformGroup: 'tokens-studio',
    buildPath: 'build/scss/',
    files: [{
      destination: '_variables.scss',
      format: 'scss/variables'
    }]
  },

  // JavaScript ES6
  js: {
    transformGroup: 'tokens-studio',
    buildPath: 'build/js/',
    files: [
      {
        destination: 'tokens.js',
        format: 'javascript/es6'
      },
      {
        destination: 'tokens.d.ts',
        format: 'typescript/es6-declarations'
      }
    ]
  },

  // JSON (flat, resolved values)
  json: {
    transformGroup: 'tokens-studio',
    buildPath: 'build/json/',
    files: [{
      destination: 'tokens.json',
      format: 'json/flat'
    }]
  }
};

// Build configuration
export default {
  // Token source files
  source: [
    'tokens/primitives/**/*.tokens.json',
    'tokens/semantic/**/*.tokens.json'
  ],

  // Enable DTCG preprocessor
  preprocessors: ['tokens-studio'],

  // Platform configurations
  platforms,

  // Uncomment to enable theme-specific builds
  // platforms: {
  //   ...Object.fromEntries(
  //     themes.map(theme => [
  //       `css-${theme}`,
  //       {
  //         ...platforms.css,
  //         buildPath: `build/css/${theme}/`,
  //         source: [`tokens/themes/${theme}/**/*.tokens.json`],
  //         files: [{
  //           destination: 'variables.css',
  //           format: 'css/variables',
  //           options: {
  //             outputReferences: true,
  //             selector: `[data-theme="${theme}"]`
  //           }
  //         }]
  //       }
  //     ])
  //   )
  // }
};
