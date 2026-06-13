import { IBrowserProvider } from '../../core/interfaces/IBrowserProvider';

export class ChromeProvider implements IBrowserProvider {
  onUrlChanged(callback: (tabId: number, newUrl: string) => void): void {
    if (typeof chrome !== 'undefined' && chrome.tabs) {
      chrome.tabs.onUpdated.addListener((tabId, changeInfo) => {
        if (changeInfo.url) {
          callback(tabId, changeInfo.url);
        }
      });
    }
  }

  sendMessage<T>(message: any): Promise<T> {
    return new Promise((resolve, reject) => {
      if (typeof chrome !== 'undefined' && chrome.runtime) {
        chrome.runtime.sendMessage(message, (response) => {
          if (chrome.runtime.lastError) {
            reject(chrome.runtime.lastError);
          } else {
            resolve(response);
          }
        });
      } else {
        reject(new Error("Chrome runtime not available."));
      }
    });
  }

  onMessage(callback: (message: any, sender: any, sendResponse: (response: any) => void) => boolean | void): void {
    if (typeof chrome !== 'undefined' && chrome.runtime) {
      chrome.runtime.onMessage.addListener(callback);
    }
  }
}
