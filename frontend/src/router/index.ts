import page from "page";
export default page;

import { tryingToLoadUser } from "../stores/user";

export function createRoute(
  path: string,
  func: () => void,
  options?: {
    middlewares: (() => boolean)[];
  }
) {
  if (options?.middlewares) {
    page(
      path,
      async (_c, next) => {
        await tryingToLoadUser;
        next();
      },
      ...options.middlewares.map((middleware) => {
        return (_c, next) => {
          if (middleware()) next();
        };
      }),
      func
    );
  } else {
    page(
      path,
      async (_c, next) => {
        await tryingToLoadUser;
        next();
      },
      func
    );
  }
}
