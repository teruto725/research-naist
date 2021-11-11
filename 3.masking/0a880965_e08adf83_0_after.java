    public AuthenticatorSelectionDialogBridge(long nativeAuthenticatorSelectionDialogView,
            Context context, ModalDialogManager modalDialogManager) {
        mNativeCardUnmaskAuthenticationSelectionDialogView = nativeAuthenticatorSelectionDialogView;
        mContext = context;
        mAuthenticatorSelectionDialog =
                new AuthenticatorSelectionDialog(context, this, modalDialogManager);
    }
