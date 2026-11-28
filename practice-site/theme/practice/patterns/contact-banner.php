<?php
/**
 * Title: Contact banner
 * Slug: practice/contact-banner
 * Categories: practice
 * Description: Places the shared Contact details block on a tinted band.
 */
?>
<!-- wp:group {"metadata":{"name":"Contact banner"},"align":"full","backgroundColor":"tint","style":{"spacing":{"padding":{"top":"var:preset|spacing|40","bottom":"var:preset|spacing|40"}}},"layout":{"type":"constrained"}} -->
<div class="wp-block-group alignfull has-tint-background-color has-background" style="padding-top:var(--wp--preset--spacing--40);padding-bottom:var(--wp--preset--spacing--40)">
<!-- wp:heading {"level":2,"fontSize":"large"} --><h2 class="wp-block-heading has-large-font-size">Contact</h2><!-- /wp:heading -->
<?php echo practice_synced( 'contact-details' ); ?>
</div>
<!-- /wp:group -->
