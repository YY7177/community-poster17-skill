$ErrorActionPreference = 'Stop'
$taskSecureKey = Read-Host 'Paste your Ark API key (input is hidden)' -AsSecureString
$taskKeyPointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($taskSecureKey)
try {
    $taskPlainKey = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($taskKeyPointer).Trim()
    if ([string]::IsNullOrWhiteSpace($taskPlainKey)) { throw 'API key cannot be empty.' }
    [Environment]::SetEnvironmentVariable('COMMUNITY_POSTER_ARK_API_KEY', $taskPlainKey, 'User')
    $env:COMMUNITY_POSTER_ARK_API_KEY = $taskPlainKey
    Write-Host 'Community poster Ark API key saved for your Windows user. The key has not been printed.'
} finally {
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($taskKeyPointer)
    $taskPlainKey = $null
    $taskSecureKey.Dispose()
}
