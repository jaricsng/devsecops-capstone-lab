import { describe, expect, it } from "vitest";

import { formatPrice } from "./client";

describe("formatPrice", () => {
  it("formats whole dollars", () => {
    expect(formatPrice(4200)).toBe("$42.00");
  });

  it("formats sub-dollar amounts", () => {
    expect(formatPrice(600)).toBe("$6.00");
  });

  it("formats zero", () => {
    expect(formatPrice(0)).toBe("$0.00");
  });
});
