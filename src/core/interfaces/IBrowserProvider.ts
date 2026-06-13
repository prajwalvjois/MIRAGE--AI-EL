export interface IBrowserProvider {
  onUrlChanged(callback: (tabId: number, newUrl: string) => void): void;
  sendMessage<T>(message: any): Promise<T>;
  onMessage(callback: (message: any, sender: any, sendResponse: (response: any) => void) => boolean | void): void;
}
