<?php
/**
 * Title: Intake: Waitlist
 * Slug: practice/booking-waitlist
 * Categories: practice-intake
 * Description: Paste into the shared "Booking action" block to switch every page to this state.
 */
?>
<!-- wp:group {"metadata":{"name":"Intake: Waitlist"},"layout":{"type":"constrained"},"style":{"spacing":{"blockGap":"0.75rem"}}} -->
<div class="wp-block-group">
<!-- wp:paragraph {"className":"practice-status is-waitlist"} --><p class="practice-status is-waitlist">Waitlist open</p><!-- /wp:paragraph -->
<!-- wp:buttons --><div class="wp-block-buttons"><!-- wp:button --><div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="https://booking.example.invalid/waitlist">Join the waitlist</a></div><!-- /wp:button --></div><!-- /wp:buttons -->
<!-- wp:paragraph {"fontSize":"small","textColor":"muted"} --><p class="has-muted-color has-text-color has-small-font-size">The current wait is about [x] weeks. <span class="practice-draft">confirm</span> We'll contact you when a place opens, and you can leave the list at any time.</p><!-- /wp:paragraph -->
</div>
<!-- /wp:group -->
