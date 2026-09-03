#pragma once
#include <string_view>
namespace sih26168::navigation {
[[nodiscard]] constexpr std::string_view contract_version() noexcept { return "1.0.0-bootstrap"; }
}
