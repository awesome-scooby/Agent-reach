<?php
/**
 * Title: Service page
 * Slug: practice/service-detail
 * Categories: practice
 * Block Types: core/post-content
 * Post Types: page
 * Description: Starting layout for a service: who it's for, what sessions involve, delivery, fee and next step.
 */
?>
<!-- wp:paragraph {"className":"practice-lead"} --><p class="practice-lead">[One sentence on who this is for.] <span class="practice-draft">practitioner to approve</span></p><!-- /wp:paragraph -->
<!-- wp:heading --><h2 class="wp-block-heading">Is this for you?</h2><!-- /wp:heading -->
<!-- wp:list --><ul class="wp-block-list"><!-- wp:list-item --><li>[A situation someone might recognise]</li><!-- /wp:list-item --><!-- wp:list-item --><li>[Another, in everyday words]</li><!-- /wp:list-item --></ul><!-- /wp:list -->
<!-- wp:heading --><h2 class="wp-block-heading">What sessions involve</h2><!-- /wp:heading -->
<!-- wp:paragraph --><p>[What a session may involve, in plain terms. No promised outcomes.]</p><!-- /wp:paragraph -->
<!-- wp:heading --><h2 class="wp-block-heading">How it's delivered</h2><!-- /wp:heading -->
<!-- wp:paragraph --><p>Telehealth (secure video) from anywhere in Australia. <a href="/how-sessions-work/">How sessions work</a></p><!-- /wp:paragraph -->
<!-- wp:heading --><h2 class="wp-block-heading">Fee</h2><!-- /wp:heading -->
<?php echo practice_synced( 'fee-standard-session' ); ?>
<!-- wp:paragraph {"className":"practice-more"} --><p class="practice-more"><a href="/fees/">All fees and rebates</a></p><!-- /wp:paragraph -->
<!-- wp:paragraph --><p>Provided by <a href="/meet/">[Name]</a>.</p><!-- /wp:paragraph -->
<?php echo practice_synced( 'booking-action' ); ?>
