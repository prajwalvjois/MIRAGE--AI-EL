export interface IEmailExtractor {
  isTargetPage(url: string): boolean;
  isEmailOpen(): boolean;
  extractBody(): string | null;
}
