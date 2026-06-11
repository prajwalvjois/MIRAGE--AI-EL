export interface IBrowserProvider {
  onUrlChanged(callback: (tabId: number, newUrl: string) => void): void;
}
