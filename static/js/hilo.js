function hiloState() {
    return {
        open: [],
        personal: false,
        mobile: false,
        init() {
            this.personal = this.$root.dataset.personal === "1";
            const media = window.matchMedia("(max-width: 860px)");
            const apply = () => {
                this.mobile = media.matches;
                const defaults = Array.from(this.$root.querySelectorAll("[data-default-open='1']")).map(
                    (button) => button.dataset.station
                );
                this.open = this.mobile || this.personal ? defaults.slice(0, 1) : defaults;
            };
            apply();
            media.addEventListener("change", apply);
        },
        isOpen(id) {
            return this.open.indexOf(id) !== -1;
        },
        toggle(id) {
            if (this.mobile || this.personal) {
                this.open = [id];
                return;
            }
            this.open = this.isOpen(id) ? this.open.filter((item) => item !== id) : this.open.concat([id]);
        },
    };
}
