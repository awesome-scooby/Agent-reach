<?php
/**
 * Title: Contact and appointments
 * Slug: practice/contact-page
 * Categories: practice
 * Description: Booking action, how to contact, what to expect, urgent help.
 */
?>
<!-- wp:paragraph {"className":"practice-lead"} --><p class="practice-lead">The quickest way to start is to book online. If you have a question first, call or email.</p><!-- /wp:paragraph -->
<?php echo practice_synced( 'booking-action' ); ?>
<!-- wp:heading --><h2 class="wp-block-heading">Contact details</h2><!-- /wp:heading -->
<?php echo practice_synced( 'contact-details' ); ?>
<!-- wp:heading --><h2 class="wp-block-heading">What to expect</h2><!-- /wp:heading -->
<!-- wp:list --><ul class="wp-block-list"><!-- wp:list-item --><li>[Name] replies to calls and emails within [2] business days. <span class="practice-draft">confirm</span></li><!-- /wp:list-item --><!-- wp:list-item --><li>Sending a message doesn't book an appointment.</li><!-- /wp:list-item --><!-- wp:list-item --><li>Please don't include health details in emails. You can share them safely in your session.</li><!-- /wp:list-item --><!-- wp:list-item --><li>If the booking site isn't working, call or email instead and we'll book you in.</li><!-- /wp:list-item --></ul><!-- /wp:list -->
