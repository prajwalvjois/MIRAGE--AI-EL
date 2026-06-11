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
}
