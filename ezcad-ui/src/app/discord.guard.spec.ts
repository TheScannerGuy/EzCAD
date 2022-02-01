import { TestBed } from '@angular/core/testing';

import { DiscordGuard } from './discord.guard';

describe('DiscordGuard', () => {
  let guard: DiscordGuard;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    guard = TestBed.inject(DiscordGuard);
  });

  it('should be created', () => {
    expect(guard).toBeTruthy();
  });
});
