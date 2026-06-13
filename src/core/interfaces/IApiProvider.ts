export interface IApiProvider {
  analyzeEmail(emailText: string): Promise<number | null>;
  analyzeUrl(url: string): Promise<number | null>;
}
